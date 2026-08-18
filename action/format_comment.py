#!/usr/bin/env python3
"""Turn diffly-cli JSON into a compact, stable PR comment."""
from __future__ import annotations

import json
import sys

MARKER = "<!-- diffly-cli:pr-triage -->"


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: format_comment.py RESULT.json")
    with open(sys.argv[1], encoding="utf-8") as handle:
        result = json.load(handle)

    metadata = result["metadata"]
    verdict = result["verdict"]
    flags = result.get("flags", [])
    checks = result.get("checks", {})
    files = result.get("files", [])
    lines_changed = metadata.get("additions", 0) + metadata.get("deletions", 0)
    flag_summary = ", ".join(f"`{item['code']}` ({item['severity']})" for item in flags) or "None"
    check_state = checks.get("state", "unknown").upper()

    out = [
        MARKER,
        f"## Diffly verdict: **{verdict}**",
        "",
        f"**{metadata['owner']}/{metadata['repo']}#{metadata['number']}** · "
        f"{metadata.get('changed_files', len(files))} files · {lines_changed} lines changed · "
        f"checks: **{check_state}**",
        "",
        f"**Risk flags:** {flag_summary}",
        "",
        "<details>",
        "<summary>Risk flags and reasoning</summary>",
        "",
    ]
    if flags:
        for item in flags:
            evidence = "; ".join(f"`{value}`" for value in item.get("evidence", [])[:8]) or "no file evidence"
            out.append(f"- **{item['code']}** ({item['severity']}): {item['message']} — {evidence}")
    else:
        out.append("No deterministic risk flags fired.")
    for reason in result.get("reasoning", []):
        out.append(f"- {reason}")
    out += ["", "</details>", "", "<details>", "<summary>Blast-radius summary</summary>", ""]
    if files:
        out.append("| File | Change | Symbols | Direct callers | Tests |")
        out.append("| --- | ---: | --- | --- | --- |")
        for item in files:
            symbols = ", ".join(f"`{x}`" for x in item.get("touched_symbols", [])) or "—"
            callers = ", ".join(f"`{x}`" for x in item.get("callers", [])) or "—"
            tests = ", ".join(f"`{x}`" for x in item.get("tests_found", [])) or "—"
            change = f"+{item.get('additions', 0)}/-{item.get('deletions', 0)}"
            out.append(f"| `{item['path']}` | {change} | {symbols} | {callers} | {tests} |")
    else:
        out.append("No changed files were returned by GitHub.")
    out += ["", "</details>", "", "_Deterministic triage is authoritative; any optional LLM explanation cannot change the verdict._"]
    print("\n".join(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
