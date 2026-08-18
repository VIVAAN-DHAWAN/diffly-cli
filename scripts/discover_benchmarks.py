#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

QUERIES = ["Claude", "Codex", "Copilot", "Cursor", "Aider", "Devin", "AI-generated"]
CUTOFF = datetime(2025, 1, 1, tzinfo=timezone.utc)
OUT = Path("/tmp/diffly-benchmark-candidates.json")


def gh_json(args: list[str]):
    raw = subprocess.check_output(["gh", *args], text=True)
    raw = re.sub(r"\x1b\[[0-9;]*m", "", raw)
    if not raw.strip():
        return []
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"GitHub returned non-JSON for {' '.join(args)}: {raw[:300]!r}") from exc


def inspect_candidate(row: dict, query: str) -> dict | None:
    repo = row["repository"]["nameWithOwner"]
    number = int(row["number"])
    created = datetime.fromisoformat(row["createdAt"].replace("Z", "+00:00"))
    if created < CUTOFF:
        return None
    try:
        detail = gh_json(["api", f"repos/{repo}/pulls/{number}"])
    except (subprocess.CalledProcessError, RuntimeError):
        return None
    files = int(detail.get("changed_files", 0))
    lines = int(detail.get("additions", 0)) + int(detail.get("deletions", 0))
    if files < 8 or lines < 300:
        return None
    return {
        "repo": repo,
        "number": number,
        "title": detail.get("title", row["title"]),
        "created_at": row["createdAt"],
        "additions": detail.get("additions", 0),
        "deletions": detail.get("deletions", 0),
        "changed_files": files,
        "url": detail.get("html_url", row["url"]),
        "query": query,
        "author": (detail.get("user") or {}).get("login", "unknown"),
    }


def main() -> None:
    seen: set[tuple[str, int]] = set()
    selected: list[dict] = []
    rows_with_queries: list[tuple[dict, str]] = []
    for query in QUERIES:
        try:
            rows = gh_json(["search", "prs", query, "--merged", "--limit", "30", "--match", "title,body", "--json", "repository,number,title,createdAt,url"])
        except (subprocess.CalledProcessError, RuntimeError) as exc:
            print(f"search failed for {query}: {exc}")
            continue
        for row in rows:
            key = (row["repository"]["nameWithOwner"], int(row["number"]))
            if key not in seen:
                seen.add(key)
                rows_with_queries.append((row, query))
    with ThreadPoolExecutor(max_workers=12) as pool:
        futures = [pool.submit(inspect_candidate, row, query) for row, query in rows_with_queries]
        for future in as_completed(futures):
            result = future.result()
            if result:
                selected.append(result)
    selected.sort(key=lambda item: (item["changed_files"], item["additions"] + item["deletions"]), reverse=True)
    OUT.write_text(json.dumps(selected, indent=2) + "\n")
    for item in selected[:80]:
        print(f"{item['repo']}#{item['number']}\t{item['changed_files']} files\t+{item['additions']}/-{item['deletions']}\t{item['query']}\t{item['title'][:100]}")
    print(f"Wrote {len(selected)} candidates to {OUT}")


if __name__ == "__main__":
    main()
