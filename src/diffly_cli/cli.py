from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter
from typing import Any

from rich.console import Console
from rich.markdown import Markdown

from .astmap import analyze_files
from .github import GitHubClient, GitHubError
from .models import ChangedFile, PRMetadata, TriageResult
from .triage import compute_flags, verdict_for

console = Console()


def parse_repo(value: str) -> tuple[str, str]:
    value = value.rstrip("/")
    if value.startswith("https://github.com/"):
        value = value.split("https://github.com/", 1)[1]
    if value.startswith("github.com/"):
        value = value.split("github.com/", 1)[1]
    parts = value.split("/")
    if len(parts) != 2 or not all(parts):
        raise argparse.ArgumentTypeError("repository must look like owner/repo")
    return parts[0], parts[1]


def summarize_checks(check_runs: dict[str, Any], status: dict[str, Any]) -> dict[str, Any]:
    runs = check_runs.get("check_runs", [])
    failed = []
    pending = []
    for run in runs:
        conclusion = run.get("conclusion")
        name = run.get("name", "unnamed check")
        if conclusion in {"failure", "cancelled", "timed_out", "action_required", "startup_failure"}:
            failed.append(name)
        elif conclusion not in {"success", "skipped", "neutral"}:
            pending.append(name)
    statuses = status.get("statuses", [])
    for item in statuses:
        state = item.get("state")
        context = item.get("context", "unnamed status")
        if state == "failure":
            failed.append(context)
        elif state in {"pending", "error"}:
            pending.append(context)
    if failed:
        state = "failure"
    elif pending:
        state = "pending"
    elif runs or statuses:
        state = "success"
    else:
        state = "unknown"
    return {"state": state, "failed": sorted(dict.fromkeys(failed)), "pending": sorted(dict.fromkeys(pending)), "count": len(runs) + len(statuses)}


def _risk_badge(severity: str) -> str:
    return {"critical": "CRITICAL", "high": "HIGH", "medium": "MEDIUM", "low": "LOW"}.get(severity, severity.upper())


def render_markdown(result: TriageResult) -> str:
    m = result.metadata
    lines = [
        f"# PR triage: [{m.owner}/{m.repo}#{m.number}]({m.html_url})",
        "",
        f"**Title:** {m.title}",
        f"**Author:** @{m.author}  ",
        f"**Refs:** `{m.base_ref}` ← `{m.head_ref}`  ",
        f"**Commits:** {m.commits} · **Files:** {m.changed_files} · **Lines:** +{m.additions} / -{m.deletions}",
        "",
        "## Verdict",
        "",
        f"# **{result.verdict}**",
        "",
        *[f"- {reason}" for reason in result.reasoning],
        "",
        "## Checks",
        "",
        f"- State: **{result.checks.get('state', 'unknown').upper()}**",
        f"- Observed checks: {result.checks.get('count', 0)}",
    ]
    if result.checks.get("failed"):
        lines.append(f"- Failed: {', '.join(f'`{x}`' for x in result.checks['failed'])}")
    if result.checks.get("pending"):
        lines.append(f"- Pending: {', '.join(f'`{x}`' for x in result.checks['pending'])}")

    lines += ["", "## Risk flags", ""]
    if result.flags:
        for flag in result.flags:
            lines.append(f"### `{flag.code}` — {_risk_badge(flag.severity)}")
            lines.append(flag.message)
            for evidence in flag.evidence[:20]:
                lines.append(f"- `{evidence}`")
            lines.append("")
    else:
        lines.append("No deterministic risk flags fired.")

    lines += ["", "## Blast-radius map", "", "The Phase 1 map is conservative: it identifies changed files, changed symbols, and direct call sites visible in changed hunks. A full repository-wide call graph is a Phase 2 enhancement.", ""]
    for file in result.files:
        lines.append(f"### `{file.path}` ({file.status}, +{file.additions}/-{file.deletions})")
        symbols = ", ".join(f"`{x}`" for x in file.touched_symbols) if file.touched_symbols else "none detected"
        callers = ", ".join(f"`{x}`" for x in file.callers) if file.callers else "none detected in changed hunks"
        tests = ", ".join(f"`{x}`" for x in file.tests_found) if file.tests_found else "none detected"
        lines.append(f"- Touched symbols: {symbols}")
        lines.append(f"- Direct callers: {callers}")
        lines.append(f"- Related tests: {tests}")
        lines.append("")

    lines += ["## Changed-file inventory", "", "| File | Status | Additions | Deletions | Symbols |", "| --- | --- | ---: | ---: | --- |"]
    for file in result.files:
        symbols = ", ".join(file.touched_symbols) if file.touched_symbols else "—"
        lines.append(f"| `{file.path}` | {file.status} | {file.additions} | {file.deletions} | {symbols} |")
    lines += ["", "## Deterministic policy", "", "- `BLOCK`: failed checks or authentication/secrets/security-sensitive changes.", "- `QUARANTINE`: database changes, dependency changes, missing obvious test coverage, or unavailable/pending checks.", "- `SHIP`: no rules fired and observed checks passed.", "", "_Generated by diffly-cli Phase 1. This output is deterministic and does not call an LLM._"]
    return "\n".join(lines) + "\n"


def build_result(client: GitHubClient, owner: str, repo: str, number: int) -> TriageResult:
    metadata = client.pull_request(owner, repo, number)
    files = client.pull_request_files(owner, repo, number)
    diff = client.pull_request_diff(owner, repo, number)
    patch_by_path = {file.path: file.patch for file in files}
    if diff and not any(file.patch for file in files):
        for path in re.findall(r"^diff --git a/(.*?) b/", diff, flags=re.MULTILINE):
            patch_by_path.setdefault(path, "")
    files = analyze_files(files)
    check_runs = client.check_runs(owner, repo, metadata.head_sha)
    status = client.commit_status(owner, repo, metadata.head_sha)
    checks = summarize_checks(check_runs, status)
    try:
        repo_paths = client.repository_tree(owner, repo, metadata.head_sha)
    except GitHubError:
        repo_paths = []
    flags = compute_flags(metadata, files, checks, repo_paths)
    verdict, reasoning = verdict_for(flags, checks)
    return TriageResult(metadata, files, flags, verdict, reasoning, checks, "GitHub REST API")


def run_pr(args: argparse.Namespace) -> int:
    owner, repo = args.repository
    client = GitHubClient(token=args.token)
    try:
        result = build_result(client, owner, repo, args.number)
    except GitHubError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        return 2
    output = render_markdown(result)
    if args.json:
        payload = {
            "metadata": result.metadata.__dict__,
            "files": [file.__dict__ for file in result.files],
            "flags": [flag.__dict__ for flag in result.flags],
            "verdict": result.verdict,
            "reasoning": result.reasoning,
            "checks": result.checks,
            "source": result.source,
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
    elif args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(output)
        console.print(f"Wrote {args.output}")
    else:
        console.print(Markdown(output))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="diffly-cli", description="Deterministic triage for large GitHub pull requests")
    subparsers = parser.add_subparsers(dest="command", required=True)
    pr = subparsers.add_parser("pr", help="Analyze one GitHub pull request")
    pr.add_argument("repository", type=parse_repo, metavar="<owner/repo>")
    pr.add_argument("number", type=int, metavar="<pr-number>")
    pr.add_argument("--token", default=None, help="GitHub token; defaults to GITHUB_TOKEN")
    pr.add_argument("--output", help="Write terminal Markdown to a file")
    pr.add_argument("--json", action="store_true", help="Emit structured JSON instead of Markdown")
    pr.set_defaults(func=run_pr)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
