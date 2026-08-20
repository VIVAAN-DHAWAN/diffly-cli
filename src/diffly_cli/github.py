from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any

from .diffparse import files_from_unified_diff
from .models import ChangedFile, PRMetadata


class GitHubError(RuntimeError):
    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


@dataclass(frozen=True)
class RepositoryTreeResult:
    paths: list[str]
    truncated: bool


class GitHubClient:
    def __init__(self, token: str | None = None, api_url: str = "https://api.github.com") -> None:
        self.token = token or os.environ.get("GITHUB_TOKEN")
        self.api_url = api_url.rstrip("/")

    def request(self, path: str, *, accept: str = "application/vnd.github+json", params: dict[str, Any] | None = None) -> Any:
        url = f"{self.api_url}{path}"
        if params:
            url += "?" + urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
        headers = {
            "Accept": accept,
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "diffly-cli/0.1.0",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        req = urllib.request.Request(url, headers=headers)
        import time
        max_retries = 3
        for attempt in range(max_retries):
            try:
                with urllib.request.urlopen(req, timeout=30) as response:
                    payload = response.read().decode("utf-8")
                    if accept.endswith("diff"):
                        return payload
                    return json.loads(payload)
            except urllib.error.HTTPError as exc:
                if exc.code in (403, 429):
                    reset = exc.headers.get("X-RateLimit-Reset")
                    retry_after = exc.headers.get("Retry-After")
                    if retry_after:
                        wait = int(retry_after)
                    elif reset:
                        wait = max(0, int(reset) - int(time.time()))
                    else:
                        wait = 2 ** attempt
                    
                    if wait < 60 and attempt < max_retries - 1:
                        time.sleep(wait)
                        continue
                    
                    auth_msg = "" if self.token else " (Unauthenticated request. Provide a GITHUB_TOKEN to increase limit.)"
                    raise GitHubError(f"GitHub API {exc.code} rate limit exceeded{auth_msg}. Retry after {wait}s.", status_code=exc.code) from exc
                    
                detail = exc.read().decode("utf-8", errors="replace")
                raise GitHubError(f"GitHub API {exc.code} for {path}: {detail[:400]}", status_code=exc.code) from exc
            except urllib.error.URLError as exc:
                raise GitHubError(f"Could not reach GitHub: {exc.reason}") from exc

    def pull_request(self, owner: str, repo: str, number: int) -> PRMetadata:
        data = self.request(f"/repos/{owner}/{repo}/pulls/{number}")
        return PRMetadata(
            owner=owner,
            repo=repo,
            number=number,
            title=data.get("title", ""),
            body=data.get("body") or "",
            state=data.get("state", "unknown"),
            author=(data.get("user") or {}).get("login", "unknown"),
            base_ref=(data.get("base") or {}).get("ref", ""),
            head_ref=(data.get("head") or {}).get("ref", ""),
            base_sha=(data.get("base") or {}).get("sha", ""),
            head_sha=(data.get("head") or {}).get("sha", ""),
            mergeable_state=data.get("mergeable_state") or "unknown",
            additions=int(data.get("additions", 0)),
            deletions=int(data.get("deletions", 0)),
            changed_files=int(data.get("changed_files", 0)),
            commits=int(data.get("commits", 0)),
            html_url=data.get("html_url", f"https://github.com/{owner}/{repo}/pull/{number}"),
        )

    def pull_request_files(self, owner: str, repo: str, number: int) -> list[ChangedFile]:
        values: list[dict[str, Any]] = []
        page = 1
        try:
            while True:
                batch = self.request(
                    f"/repos/{owner}/{repo}/pulls/{number}/files",
                    params={"per_page": 100, "page": page},
                )
                values.extend(batch)
                if len(batch) < 100:
                    break
                page += 1
        except GitHubError as exc:
            if "404" not in str(exc):
                raise
            return files_from_unified_diff(self.pull_request_diff(owner, repo, number))
        return [
            ChangedFile(
                path=item.get("filename", ""),
                status=item.get("status", "modified"),
                additions=int(item.get("additions", 0)),
                deletions=int(item.get("deletions", 0)),
                changes=int(item.get("changes", 0)),
                patch=item.get("patch") or "",
            )
            for item in values
        ]

    def pull_request_diff(self, owner: str, repo: str, number: int) -> str:
        return self.request(
            f"/repos/{owner}/{repo}/pulls/{number}",
            accept="application/vnd.github.v3.diff",
        )

    def commits(self, owner: str, repo: str, number: int) -> list[dict[str, Any]]:
        values: list[dict[str, Any]] = []
        page = 1
        while True:
            batch = self.request(
                f"/repos/{owner}/{repo}/pulls/{number}/commits",
                params={"per_page": 100, "page": page},
            )
            values.extend(batch)
            if len(batch) < 100:
                break
            page += 1
        return values

    def check_runs(self, owner: str, repo: str, ref: str) -> dict[str, Any]:
        first: dict[str, Any] | None = None
        values: list[dict[str, Any]] = []
        page = 1
        while True:
            data = self.request(
                f"/repos/{owner}/{repo}/commits/{ref}/check-runs",
                params={"per_page": 100, "page": page},
            )
            if first is None:
                first = dict(data)
            batch = data.get("check_runs", [])
            if not isinstance(batch, list):
                raise GitHubError("GitHub check-runs response contained a non-list check_runs value")
            values.extend(batch)
            total = data.get("total_count")
            if len(batch) < 100 or (isinstance(total, int) and len(values) >= total):
                break
            page += 1
        result = first or {}
        result["check_runs"] = values
        result["total_count"] = len(values)
        return result

    def commit_status(self, owner: str, repo: str, ref: str) -> dict[str, Any]:
        first: dict[str, Any] | None = None
        values: list[dict[str, Any]] = []
        page = 1
        while True:
            data = self.request(
                f"/repos/{owner}/{repo}/commits/{ref}/status",
                params={"per_page": 100, "page": page},
            )
            if first is None:
                first = dict(data)
            batch = data.get("statuses", [])
            if not isinstance(batch, list):
                raise GitHubError("GitHub status response contained a non-list statuses value")
            values.extend(batch)
            total = data.get("total_count")
            if len(batch) < 100 or (isinstance(total, int) and len(values) >= total):
                break
            page += 1
        result = first or {}
        result["statuses"] = values
        result["total_count"] = len(values)
        return result

    def repository_tree(self, owner: str, repo: str, ref: str) -> RepositoryTreeResult:
        data = self.request(f"/repos/{owner}/{repo}/git/trees/{urllib.parse.quote(ref, safe='')}", params={"recursive": 1})
        paths = [item.get("path", "") for item in data.get("tree", []) if item.get("type") == "blob"]
        return RepositoryTreeResult(paths=paths, truncated=bool(data.get("truncated", False)))

    @staticmethod
    def to_json(value: Any) -> str:
        return json.dumps(value, indent=2, sort_keys=True)
