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
        raise SystemExit(f"GitHub API {exc.code}: {detail[:500]}") from exc


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
    page = 1
    existing = []
    while True:
        batch = request(f"{base}?per_page=100&page={page}", token)
        existing.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    match = next((item for item in existing if MARKER in (item.get("body") or "")), None)
    if match:
        request(f"{base}/{match['id']}", token, "PATCH", {"body": body})
        print(f"Updated Diffly comment {match['id']}")
    else:
        created = request(base, token, "POST", {"body": body})
        print(f"Created Diffly comment {created.get('id', 'unknown')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
