#!/usr/bin/env python3
"""Create or update the single Diffly comment on a pull request."""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

MARKER = "<!-- diffly-cli:pr-triage -->"
API_VERSION = "2022-11-28"


class GitHubApiError(RuntimeError):
    def __init__(self, code: int, detail: str) -> None:
        super().__init__(f"GitHub API {code}: {detail}")
        self.code = code


def request(url: str, token: str, method: str = "GET", payload: dict | None = None):
    body = json.dumps(payload).encode() if payload is not None else None
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": "diffly-cli-action",
        "X-GitHub-Api-Version": API_VERSION,
    }
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            raw = response.read().decode()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")
        raise GitHubApiError(exc.code, detail[:500]) from exc


def existing_comments(base: str, token: str) -> list:
    """List prior PR comments; a 404 means none are readable yet."""
    comments = []
    page = 1
    while True:
        try:
            batch = request(f"{base}?per_page=100&page={page}", token)
        except GitHubApiError as exc:
            if exc.code == 404 and page == 1:
                return []
            raise
        if not isinstance(batch, list):
            raise SystemExit(f"GitHub returned unexpected comment listing: {type(batch).__name__}")
        comments.extend(batch)
        if len(batch) < 100:
            return comments
        page += 1


def main() -> int:
    if len(sys.argv) != 4:
        raise SystemExit("usage: post_comment.py OWNER/REPO PR_NUMBER COMMENT_FILE; GITHUB_TOKEN must be set")
    repository, number, comment_file = sys.argv[1:]
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise SystemExit("GITHUB_TOKEN is required")
    with open(comment_file, encoding="utf-8") as handle:
        body = handle.read()
    base = f"https://api.github.com/repos/{repository}/issues/{number}/comments"
    match = next((item for item in existing_comments(base, token) if MARKER in (item.get("body") or "")), None)
    try:
        if match:
            request(f"{base}/{match['id']}", token, "PATCH", {"body": body})
            print(f"Updated Diffly comment {match['id']}")
        else:
            created = request(base, token, "POST", {"body": body})
            print(f"Created Diffly comment {created.get('id', 'unknown')}")
    except GitHubApiError as exc:
        if exc.code == 404:
            print("Warning: Diffly could not publish its PR comment (GitHub returned 404; check pull-request write permissions).")
        else:
            raise
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
