#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# One PR per repository where practical, selected for distinct languages, repository sizes,
# and visible agent/tool attribution in the title or search context.
SELECTED = [
    ("workcrewlabs/worker-pc-app", 45),
    ("Kirt22/Journal.IO-mono-repo", 70),
    ("ferrreo/local-image-detect-chrome", 7),
    ("laurilehtinen/ccusage", 2),
    ("attunehq/nudge", 72),
    ("joangarvin/travseeker", 22),
    ("powabase-ai/powabase-ai", 46),
    ("Cagatay342/openusage", 1),
    ("fwaris/FsHarness", 4),
    ("corosolto/client", 205),
    ("ycoj/YCOJ", 18),
    ("springbrand-lab/springbrand-agent-setup", 13),
    ("xiaoqiuuuu/Codex-Pulse", 3),
    ("JinnZ2/CEED", 2),
    ("flatpark/flatpark", 211),
    ("vshulcz/deja-vu", 396),
    ("augentic/omnia-backends", 55),
    ("Gegcuk/QuizMaker", 756),
]
OUT = Path("/tmp/diffly-benchmark-results.json")


def gh_json(path: str) -> dict:
    raw = subprocess.check_output(["gh", "api", path], text=True)
    raw = re.sub(r"\x1b\[[0-9;]*m", "", raw)
    return json.loads(raw)


def run_one(repo: str, number: int, token: str) -> dict:
    try:
        pr = gh_json(f"repos/{repo}/pulls/{number}")
        repo_info = gh_json(f"repos/{repo}")
    except (subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        return {"repo": repo, "number": number, "error": str(exc)}
    command = ["diffly-cli", "pr", repo, str(number), "--token", token, "--json"]
    completed = subprocess.run(command, check=False, capture_output=True, text=True)
    if completed.returncode != 0:
        return {"repo": repo, "number": number, "error": completed.stderr[-1000:] or completed.stdout[-1000:]}
    result = json.loads(completed.stdout)
    metadata = result["metadata"]
    flags = result.get("flags", [])
    changed_lines = metadata["additions"] + metadata["deletions"]
    # Proxy, not an observed measurement: 300 changed lines/hour plus one minute/file
    # for context switching, versus two minutes for the compact Diffly page plus 10 sec/file.
    raw_minutes = changed_lines / 5.0 + metadata["changed_files"]
    diffly_minutes = 2.0 + metadata["changed_files"] / 6.0
    return {
        "repo": repo,
        "number": number,
        "url": metadata["html_url"],
        "title": pr.get("title", ""),
        "author": (pr.get("user") or {}).get("login", "unknown"),
        "created_at": pr.get("created_at", ""),
        "merged_at": pr.get("merged_at", ""),
        "language": repo_info.get("language") or "Unknown",
        "stars": repo_info.get("stargazers_count", 0),
        "pushed_at": repo_info.get("pushed_at", ""),
        "files": metadata["changed_files"],
        "additions": metadata["additions"],
        "deletions": metadata["deletions"],
        "lines": changed_lines,
        "verdict": result["verdict"],
        "flags": [
            {"code": flag["code"], "severity": flag["severity"], "message": flag["message"], "evidence": flag.get("evidence", [])[:6]}
            for flag in flags
        ],
        "checks": result.get("checks", {}),
        "raw_minutes": round(raw_minutes, 1),
        "diffly_minutes": round(diffly_minutes, 1),
    }


def main() -> None:
    token = os.environ.get("GITHUB_TOKEN") or subprocess.check_output(["gh", "auth", "token"], text=True).strip()
    results = []
    with ThreadPoolExecutor(max_workers=5) as pool:
        futures = [pool.submit(run_one, repo, number, token) for repo, number in SELECTED]
        for future in as_completed(futures):
            results.append(future.result())
            item = results[-1]
            print(f"{item['repo']}#{item['number']}: {item.get('verdict', 'ERROR')} ({item.get('files', '?')} files, {item.get('lines', '?')} lines)", flush=True)
    results.sort(key=lambda item: (item["repo"], item["number"]))
    OUT.write_text(json.dumps(results, indent=2) + "\n")
    print(f"Wrote {len(results)} benchmark results to {OUT}")


if __name__ == "__main__":
    main()
