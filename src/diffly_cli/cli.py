from __future__ import annotations

import argparse
import json
from contextlib import nullcontext
from dataclasses import asdict, dataclass
import os
import re
import select
import shutil
import sys
import time
from typing import Any

from rich.align import Align
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table
from rich.text import Text

from . import __version__
from . import update
from .astmap import analyze_files
from .explainer import ExplanationResult, generate_explanation
from .diffparse import files_from_unified_diff
from .github import GitHubClient, GitHubError
from .local import LocalAnalysisError, build_local_result, resolve_repository_root
from .models import ChangedFile, PRMetadata, TriageResult
from .triage import compute_flags, verdict_for

console = Console()
VERDICT_STYLES = {"PASS": "bold green", "SHIP": "bold green", "QUARANTINE": "bold yellow", "BLOCK": "bold red"}
CONTENT_WIDTH = 100
INTERACTIVE_SECTIONS = (
    ("verdict", "Verdict", "The decision and the reasons behind it"),
    ("checks", "Checks", "The latest CI and commit-status results"),
    ("risks", "Risk flags", "Changes that need extra review"),
    ("files", "Changed files", "The scope of the pull request"),
)


def center(renderable: Any) -> Any:
    """Horizontally center a renderable so screens feel composed, not left-hugging."""
    return Align.center(renderable, style="")


def center_screen(renderable: Any, *, estimated_height: int) -> None:
    """Clear the terminal and place a small interactive screen near its centre."""
    console.clear()
    top_padding = max((console.size.height - estimated_height) // 2, 0)
    if top_padding:
        console.print("\n" * top_padding, end="")
    console.print(center(renderable))


def _loading_mark(turn: str) -> Text:
    """Render a terminal-safe stand-in for the existing Diffly logo.

    Rich targets ordinary text terminals, where raster-image rotation is not
    portable. The repository logo remains unchanged in ``assets/logo.png``;
    this small + / − mark mirrors it for the short terminal animation.
    """
    mark = Text(justify="center")
    mark.append("⬡ ", style="bold cyan")
    mark.append("+ / −", style="bold white")
    mark.append(f" {turn}", style="bold cyan")
    return mark


def show_loading_screen(message: str) -> None:
    """Play a short, reduced-motion-friendly loading transition for TTY users."""
    if not sys.stdout.isatty():
        return
    # Enter centre quickly, turn clockwise, pause, then settle upright.
    frames = (("", 0.08), ("↻", 0.10), ("↻", 0.30), ("", 0.10))
    for turn, duration in frames:
        screen = Panel.fit(
            Text.assemble(
                _loading_mark(turn),
                "\n\n",
                (message, "dim"),
            ),
            border_style="cyan",
            padding=(1, 4),
        )
        center_screen(screen, estimated_height=8)
        time.sleep(duration)


def interactive_sections(explanation: ExplanationResult | None) -> list[tuple[str, str, str]]:
    """Return the report sections shown in the keyboard-driven review menu."""
    sections = list(INTERACTIVE_SECTIONS)
    if explanation is not None:
        sections.append(("explain", "Explanation", "Optional generated context; never changes the verdict"))
    return sections


@dataclass(frozen=True)
class RepoRef:
    """A repository reference, optionally carrying a PR number from a URL."""

    owner: str
    repo: str
    pr_number: int | None = None

    @property
    def slug(self) -> str:
        return f"{self.owner}/{self.repo}"


def positive_pr_number(value: str) -> int:
    """Parse a GitHub pull-request number, rejecting impossible values early."""
    if not value.isdigit():
        raise argparse.ArgumentTypeError("PR number must be an integer greater than zero")
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("PR number must be greater than zero")
    return number


def _normalize_github_path(value: str) -> str:
    value = value.strip().rstrip("/")
    for prefix in ("https://github.com/", "github.com/"):
        if value.startswith(prefix):
            return value.split(prefix, 1)[1]
    return value


def _split_owner_repo(value: str) -> tuple[str, str]:
    parts = value.split("/")
    if len(parts) != 2 or not all(parts) or any(not re.fullmatch(r"[A-Za-z0-9_.-]+", part) for part in parts):
        raise argparse.ArgumentTypeError("repository must look like owner/repo")
    return parts[0], parts[1]


def parse_repo(value: str) -> RepoRef:
    """Accept `owner/repo`, GitHub URLs, or full pull-request URLs.

    A trailing `/pull/<number>` populates `pr_number`, letting reviewers paste
    a complete pull-request link as the only positional argument.
    """
    path = _normalize_github_path(value)
    url_match = re.fullmatch(r"(.+?)/pull/(\d+)", path)
    pr_number: int | None = None
    if url_match:
        path, raw_number = url_match.groups()
        try:
            pr_number = positive_pr_number(raw_number)
        except argparse.ArgumentTypeError as exc:
            raise argparse.ArgumentTypeError(f"invalid pull-request URL: {exc}") from exc
    owner, repo = _split_owner_repo(path)
    return RepoRef(owner, repo, pr_number)


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
    combined_state = status.get("state")
    if combined_state in {"failure", "error"}:
        failed.append("combined commit status")
    elif combined_state == "pending":
        pending.append("combined commit status")
    statuses = status.get("statuses", [])
    for item in statuses:
        state = item.get("state")
        context = item.get("context", "unnamed status")
        if state in {"failure", "error"}:
            failed.append(context)
        elif state == "pending":
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


def render_explanation(explanation: ExplanationResult) -> list[str]:
    lines = ["## Literate diff — generated explanation", ""]
    if explanation.error:
        lines.extend([
            f"> Generated explanation unavailable: {explanation.error}",
            f"> Redactions applied before any model call: {explanation.redactions}",
            "",
        ])
        return lines
    lines.extend([
        f"> Generated by `{explanation.model}` from bounded, redacted context. This prose cannot change the deterministic verdict.",
        f"> Redactions applied before the model call: {explanation.redactions}",
        "",
        "### Background",
        "",
        explanation.explanation["background"],
        "",
        "### Intent in plain language",
        "",
        explanation.explanation["intent"],
        "",
        "### Narrative",
        "",
    ])
    for index, step in enumerate(explanation.explanation["narrative"], start=1):
        lines.append(f"#### {index}. {step['title']}")
        lines.append("")
        lines.append(step["explanation"])
        if step["files"]:
            lines.append(f"- Files: {', '.join(f'`{path}`' for path in step['files'])}")
        if step["evidence"]:
            lines.append(f"- Evidence: {'; '.join(step['evidence'])}")
        if step["snippet"]:
            lines.extend(["", "```text", step["snippet"], "```"])
        lines.append("")
    if explanation.explanation["review_questions"]:
        lines.extend(["### Review questions", ""])
        lines.extend(f"- {question}" for question in explanation.explanation["review_questions"])
        lines.append("")
    if explanation.explanation["uncertainties"]:
        lines.extend(["### Uncertainties", ""])
        lines.extend(f"- {item}" for item in explanation.explanation["uncertainties"])
        lines.append("")
    return lines


def render_markdown(result: TriageResult, explanation: ExplanationResult | None = None) -> str:
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

    if explanation is not None:
        lines += [""] + render_explanation(explanation)

    lines += ["## Changed-file inventory", "", "| File | Status | Additions | Deletions | Symbols |", "| --- | --- | ---: | ---: | --- |"]
    for file in result.files:
        symbols = ", ".join(file.touched_symbols) if file.touched_symbols else "—"
        lines.append(f"| `{file.path}` | {file.status} | {file.additions} | {file.deletions} | {symbols} |")
    lines += ["", "## Deterministic policy", "", "- `BLOCK`: failed checks or authentication/secrets/security-sensitive changes.", "- `QUARANTINE`: database changes, dependency changes, missing obvious production test coverage, or unavailable/pending checks.", "- `PASS`: no blocking or quarantine rule fired and observed checks passed.", "", "_Generated by diffly. Deterministic triage is authoritative; any literate-diff prose is optional generated explanation._"]
    return "\n".join(lines) + "\n"


def _progress(message: str):
    """Spinner in terminals; silent no-op for pipes and CI."""
    if sys.stdout.isatty():
        return console.status(message, spinner="dots")
    return nullcontext()


def _explanation_lines(explanation: ExplanationResult) -> list[str]:
    """Render the literate-diff explanation as compact lines for the interactive view."""
    if explanation.error:
        hint = ""
        if "API key" in explanation.error:
            hint = "\n[dim]Enable it: export DIFFLY_LLM_API_KEY=... (optional — deterministic triage is unaffected)[/]"
        return [f"[yellow]Generated explanation unavailable:[/] {explanation.error}", hint or "[dim]Deterministic triage above remains authoritative.[/]", ""]
    data = explanation.explanation
    lines = [f"[dim]Generated by {explanation.model} from bounded, redacted context · cannot change the verdict[/]", "", f"[bold]Background.[/] {data['background']}", f"[bold]Intent.[/] {data['intent']}", "", "[bold]Narrative steps[/]"]
    for index, step in enumerate(data["narrative"], start=1):
        lines.append(f"  {index}. [cyan]{step['title']}[/] — {step['explanation']}")
        if step["files"]:
            lines.append(f"     [dim]files:[/] {', '.join(step['files'])}")
    if data["review_questions"]:
        lines += ["", "[bold]Review questions[/]"] + [f"  • {question}" for question in data["review_questions"]]
    if data["uncertainties"]:
        lines += ["", "[bold]Uncertainties[/]"] + [f"  ? {item}" for item in data["uncertainties"]]
    return lines


def _section_lines(result: TriageResult, section: str, explanation: ExplanationResult | None = None) -> list[str]:
    """Build a compact Rich-friendly section for the interactive view."""
    if section == "verdict":
        style = VERDICT_STYLES.get(result.verdict, "bold")
        return [f"[{style}]{result.verdict}[/]", *result.reasoning]
    if section == "checks":
        checks = result.checks
        state = checks.get("state", "unknown").upper()
        if state == "NOT_APPLICABLE":
            return ["CI checks do not apply to local analysis."]
        return [f"State: {state}", f"Observed: {checks.get('count', 0)}", *[f"Failed: {x}" for x in checks.get("failed", [])], *[f"Pending: {x}" for x in checks.get("pending", [])]]
    if section == "risks":
        if not result.flags:
            return ["No deterministic risk flags fired."]
        return [f"{flag.code} ({flag.severity}): {flag.message}" for flag in result.flags]
    if section == "explain":
        if explanation is None:
            return ["No generated explanation requested."]
        return _explanation_lines(explanation)
    return [f"{item.path}  +{item.additions}/-{item.deletions}" for item in result.files[:80]] or ["No changed files returned."]


def interactive_view(result: TriageResult, explanation: ExplanationResult | None = None) -> None:
    """Let a reviewer choose the report sections to include with the keyboard."""
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        console.print("[yellow]Interactive review needs a terminal. Showing the full report instead.[/]")
        console.print(Markdown(render_markdown(result, explanation)))
        return
    try:
        import termios
        import tty
    except ImportError:
        console.print("[yellow]Interactive review is unavailable on this platform. Showing the full report instead.[/]")
        console.print(Markdown(render_markdown(result, explanation)))
        return
    labels = interactive_sections(explanation)
    enabled = {key: True for key, _, _ in labels}
    cursor = 0
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        while True:
            menu = Table(show_header=False, box=None, padding=(0, 1), expand=False)
            menu.add_column("", width=2)
            menu.add_column("Section", min_width=16)
            menu.add_column("Description", min_width=32)
            menu.add_column("", justify="right", width=9)
            for index, (key, label, description) in enumerate(labels):
                marker = "[bold cyan]›[/]" if index == cursor else " "
                state = "[bold green]Included[/]" if enabled[key] else "[dim]Hidden[/]"
                menu.add_row(marker, f"[bold]{label}[/]", f"[dim]{description}[/]", state)
            screen = Panel(
                menu,
                title="[bold cyan]DIFFLY[/]  [bold]Build your review[/]",
                subtitle="[dim]↑ ↓ move  ·  Space include or hide  ·  Enter show review  ·  q quit[/]",
                border_style="cyan",
                padding=(1, 2),
            )
            center_screen(screen, estimated_height=len(labels) + 7)
            key = sys.stdin.read(1)
            if key in {"q", "Q"}:
                return
            if key in {"\r", "\n"}:
                break
            if key == " ":
                selected = labels[cursor][0]
                enabled[selected] = not enabled[selected]
            elif key == "\x1b":
                sequence = _read_escape_sequence()
                if sequence == "[A":
                    cursor = (cursor - 1) % len(labels)
                elif sequence == "[B":
                    cursor = (cursor + 1) % len(labels)
        result_table = Table(show_header=True, header_style="bold cyan", box=None, padding=(0, 1))
        result_table.add_column("Section", style="cyan")
        result_table.add_column("Review details", max_width=CONTENT_WIDTH - 22)
        for key, label, _ in labels:
            if enabled[key]:
                details = "\n".join(_section_lines(result, key, explanation))
                result_table.add_row(label, details)
        screen = Panel(
            result_table,
            title=f"[bold cyan]DIFFLY REVIEW[/]  [bold]{result.metadata.owner}/{result.metadata.repo}#{result.metadata.number}[/]",
            subtitle="[dim]Focused review generated from your selected sections[/]",
            border_style="green",
            padding=(1, 2),
        )
        center_screen(screen, estimated_height=min(console.size.height, len(labels) * 5 + 7))
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def build_result(client: GitHubClient, owner: str, repo: str, number: int) -> TriageResult:
    metadata = client.pull_request(owner, repo, number)
    files = client.pull_request_files(owner, repo, number)
    try:
        diff = client.pull_request_diff(owner, repo, number)
    except GitHubError:
        # GitHub refuses raw diffs above its size limit, while the paginated
        # list-files endpoint can still provide useful metadata and patches.
        diff = ""
    if diff and any(not file.patch for file in files):
        fallback_patches = {file.path: file.patch for file in files_from_unified_diff(diff)}
        for file in files:
            if not file.patch and file.path in fallback_patches:
                file.patch = fallback_patches[file.path]
    files = analyze_files(files)
    check_runs = client.check_runs(owner, repo, metadata.head_sha)
    status = client.commit_status(owner, repo, metadata.head_sha)
    checks = summarize_checks(check_runs, status)
    try:
        tree_result = client.repository_tree(owner, repo, metadata.head_sha)
        repo_paths = tree_result.paths
        tree_truncated = tree_result.truncated
    except GitHubError:
        repo_paths = []
        tree_truncated = True
    checks = dict(checks)
    checks["repository_tree_complete"] = not tree_truncated
    if tree_truncated:
        checks["repository_tree_truncated"] = True
    flags = compute_flags(metadata, files, checks, repo_paths)
    verdict, reasoning = verdict_for(flags, checks)
    return TriageResult(metadata, files, flags, verdict, reasoning, checks, "GitHub REST API")


def result_payload(result: TriageResult, explanation: ExplanationResult | None) -> dict[str, Any]:
    return {
        "metadata": asdict(result.metadata),
        "files": [asdict(file) for file in result.files],
        "flags": [asdict(flag) for flag in result.flags],
        "verdict": result.verdict,
        "legacy_verdict": "SHIP" if result.verdict == "PASS" else result.verdict,
        "reasoning": result.reasoning,
        "checks": result.checks,
        "source": result.source,
        "literate_diff": ({
            "explanation": explanation.explanation,
            "redactions": explanation.redactions,
            "model": explanation.model,
            "error": explanation.error,
        } if explanation is not None else None),
    }


def _emit_report(result: TriageResult, explanation: ExplanationResult | None, args: argparse.Namespace) -> int:
    """Shared output tail: interactive screen, JSON, file, or terminal Markdown."""
    wants_interactive = getattr(args, "interactive", False)
    if wants_interactive and not args.json and not args.output:
        interactive_view(result, explanation)
        return 0
    output = render_markdown(result, explanation)
    if args.json:
        print(json.dumps(result_payload(result, explanation), indent=2, sort_keys=True))
    elif args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(output)
        console.print(f"Wrote {args.output}")
    else:
        console.print(Markdown(output))
    return 0


def render_pr_error(ref: RepoRef, number: int, error: GitHubError) -> None:
    """Show a concise recovery message for a failed pull-request lookup."""
    if "GitHub API 404" in str(error):
        body = (
            f"[bold red]Pull request not found[/]\n"
            f"[dim]{ref.slug}#{number} is unavailable. Check the repository, pull-request number, and your access.[/]\n\n"
            "[dim]Private repositories require GITHUB_TOKEN. You can also paste the full pull-request URL to avoid entering the number manually.[/]"
        )
    else:
        body = (
            f"[bold red]Unable to inspect pull request[/]\n{error}\n\n"
            "[dim]Check GITHUB_TOKEN, repository access, and your network connection. Run `diffly doctor` for diagnostics.[/]"
        )
    console.print(center(Panel.fit(body, border_style="red", padding=(1, 2))))


def run_pr(args: argparse.Namespace) -> int:
    ref: RepoRef = args.repository
    number = args.number if args.number is not None else ref.pr_number
    if number is None:
        console.print("[red]Error:[/red] a pull-request number is required, or pass a full pull-request URL as the repository.")
        return 2
    owner, repo = ref.owner, ref.repo
    client = GitHubClient(token=args.token)
    try:
        if getattr(args, "interactive", False):
            show_loading_screen("Preparing your review…")
        with _progress(f"[cyan]Analyzing [bold]{ref.slug}#{number}[/] — fetching metadata, diffs, symbols, and checks…[/]"):
            result = build_result(client, owner, repo, number)
    except GitHubError as exc:
        render_pr_error(ref, number, exc)
        return 2
    if args.explain:
        with _progress("[cyan]Generating literate-diff explanation…[/]"):
            explanation = generate_explanation(
                result,
                model=args.llm_model,
                base_url=args.llm_base_url,
            )
    else:
        explanation = None
    if not getattr(args, "json", False):
        console.print()
        console.print(center(Text.from_markup("[dim]Analysis complete — rendering your focused review.[/]")))
        console.print()
    return _emit_report(result, explanation, args)


def run_local(args: argparse.Namespace) -> int:
    """Triage local git changes entirely offline — no GitHub, no token."""
    scope = f"vs {args.base}" if args.base else "working tree"
    try:
        root = resolve_repository_root(args.path)
    except LocalAnalysisError as exc:
        console.print(center(Panel.fit(f"[bold red]Cannot analyze folder[/]\n{exc}\n\n[dim]Local mode works on any git checkout — including private or deleted repositories you still have on disk.[/]", border_style="red")))
        return 2
    try:
        if getattr(args, "interactive", False):
            show_loading_screen("Preparing your local review…")
        with _progress(f"[cyan]Analyzing [bold]{root.name}[/] ({scope}) — reading diffs and symbols locally…[/]"):
            result = build_local_result(str(root), base=args.base)
    except LocalAnalysisError as exc:
        console.print(center(Panel.fit(f"[bold red]Local analysis failed[/]\n{exc}", border_style="red")))
        return 2
    if args.explain:
        with _progress("[cyan]Generating literate-diff explanation…[/]"):
            explanation = generate_explanation(
                result,
                model=args.llm_model,
                base_url=args.llm_base_url,
            )
    else:
        explanation = None
    if not getattr(args, "json", False):
        console.print()
        console.print(center(Text.from_markup("[dim]Analysis complete — rendering your focused review.[/]")))
        console.print()
    return _emit_report(result, explanation, args)


def run_doctor(_: argparse.Namespace) -> int:
    """Print actionable local diagnostics without making a GitHub request."""
    table = Table(title="diffly doctor", box=None, padding=(0, 2))
    table.add_column("Check", style="cyan")
    table.add_column("Status")
    pref = update.get_update_preference()
    update_status = {"auto": "auto-update enabled", "manual": "manual updates"}.get(pref, "not set (will prompt on startup)")
    checks = [("Python", f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"), ("GitHub token", "configured" if os.environ.get("GITHUB_TOKEN") else "not set (public API only)"), ("Terminal", "interactive" if sys.stdin.isatty() else "non-interactive"), ("diffly executable", shutil.which("diffly") or "not on PATH"), ("Update preference", update_status)]
    for name, value in checks:
        table.add_row(name, value)
    console.print()
    console.print(center(table))
    console.print()
    return 0


def run_help(args: argparse.Namespace) -> int:
    args.root_parser.print_help()
    return 0


def run_version(_: argparse.Namespace) -> int:
    console.print()
    console.print(center(Text.from_markup(f"[bold cyan]diffly[/] {__version__}")))
    console.print()
    return 0


def _prompt_update(latest_version: str) -> None:
    """Ask the user whether to update now and whether to enable auto-updates.

    Called when a newer version is available and the user has not opted into
    automatic updates.  The function handles the full interactive flow:
    download-now prompt, installation, and the follow-up auto-update question.
    """
    console.print()
    console.print(
        center(
            Panel.fit(
                f"[bold cyan]diffly[/] [bold yellow]{latest_version}[/] is available "
                f"([dim]installed: {__version__}[/])\n\n"
                "[dim]Release notes: https://github.com/VIVAAN-DHAWAN/diffly-cli/releases[/]",
                border_style="yellow",
                padding=(1, 3),
            )
        )
    )
    if not Confirm.ask(
        "[cyan]Download and install the update now?[/]",
        default=True,
    ):
        console.print("[dim]Skipping update — you can run [bold]diffly update[/] later.[/]")
        return

    with _progress(f"[cyan]Updating diffly to {latest_version}…[/]"):
        success = update.install_update()

    if success:
        console.print(
            center(
                Panel.fit(
                    f"[bold green]Updated to diffly {latest_version}[/]\n\n"
                    "[dim]Restart diffly to use the new version.[/]",
                    border_style="green",
                    padding=(1, 2),
                )
            )
        )
        if Confirm.ask(
            "[cyan]Would you like diffly to automatically update in the future?[/]",
            default=False,
        ):
            update.set_update_preference("auto")
            console.print("[dim]Auto-update enabled — diffly will update itself when new versions are released.[/]")
        else:
            update.set_update_preference("manual")
            console.print("[dim]Manual updates — diffly will prompt you when a new version is available.[/]")
    else:
        console.print(
            center(
                Panel.fit(
                    "[bold red]Update failed[/]\n\n"
                    "[dim]Try running [bold]diffly update[/] or re-run the install script manually:\n"
                    "curl -fsSL https://raw.githubusercontent.com/VIVAAN-DHAWAN/diffly-cli/main/install.sh | sh[/]",
                    border_style="red",
                    padding=(1, 2),
                )
            )
        )


def _check_and_prompt_update(*, skip_auto: bool = False) -> None:
    """Check for updates and act according to the user's stored preference.

    - ``auto``: silently install the update (unless *skip_auto* is true).
    - ``manual`` or unset: prompt the user interactively.
    - Non-interactive terminals: skip entirely.
    """
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        return

    latest = update.check_for_update()
    if latest is None:
        return

    preference = update.get_update_preference()
    if preference == "auto" and not skip_auto:
        with _progress(f"[cyan]Auto-updating diffly to {latest}…[/]"):
            if update.install_update():
                console.print(
                    center(
                        Panel.fit(
                            f"[bold green]Auto-updated to diffly {latest}[/]",
                            border_style="green",
                            padding=(1, 2),
                        )
                    )
                )
                console.print()
                sys.exit(0)
        return

    _prompt_update(latest)


def run_update(_: argparse.Namespace) -> int:
    """Manually check for and install the latest diffly release."""
    console.print()
    latest = update.check_for_update()
    if latest is None:
        console.print(
            center(
                Panel.fit(
                    f"[bold green]diffly {__version__} is up to date[/]\n\n"
                    "[dim]No newer release was found on PyPI.[/]",
                    border_style="green",
                    padding=(1, 2),
                )
            )
        )
        return 0
    _prompt_update(latest)
    return 0


def run_wizard(parser: argparse.ArgumentParser) -> int:
    """Run the zero-argument first-use flow for human reviewers."""
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        parser.print_help()
        return 2
    console.clear()
    _check_and_prompt_update()
    console.print()
    console.print(center(Panel.fit(
        "[bold cyan]diffly[/]  [dim]Deterministic pull-request triage[/]\n"
        "[bold]Start a focused review[/] by pasting a GitHub repository or pull-request URL.",
        border_style="cyan",
        padding=(1, 4),
    )))
    console.print(center(Text.from_markup("[dim]Tip: for scripts and CI, use `diffly pr OWNER/REPO NUMBER --json`.\n[/]")))
    console.print(center(Text.from_markup("[dim]Accepted: owner/repo, a GitHub repository URL, or a full pull-request URL.[/]\n")))
    while True:
        raw_repository = Prompt.ask(
            "[cyan]Repository or pull-request URL[/]",
            default=os.environ.get("DIFFLY_REPOSITORY", ""),
            show_default=False,
        )
        try:
            reference = parse_repo(raw_repository)
            break
        except argparse.ArgumentTypeError as exc:
            console.print(f"[red]That repository address is not valid.[/] {exc}\n[dim]Use owner/repo or paste a GitHub repository or pull-request URL.[/]")
    if reference.pr_number is not None:
        number = reference.pr_number
        console.print(f"[dim]Pull request #{number} was found in the URL.[/]")
    else:
        while True:
            raw_number = Prompt.ask(f"[cyan]Pull-request number for {reference.slug}[/]")
            try:
                number = positive_pr_number(raw_number)
                break
            except argparse.ArgumentTypeError as exc:
                console.print(f"[red]That pull-request number is not valid.[/] {exc}")
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        console.print("[dim]No GitHub token found. Public repositories still work, with lower API limits.[/]")
    llm_key = os.environ.get("DIFFLY_LLM_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if llm_key:
        explain = Confirm.ask(
            "[cyan]Include an optional AI explanation?[/] [dim]It uses your configured API key and never changes the verdict.[/]",
            default=False,
        )
    else:
        explain = False
        console.print(
            "[yellow]AI explanation is not configured.[/] "
            "[dim]Set DIFFLY_LLM_API_KEY (or OPENAI_API_KEY) to enable it; the deterministic review is ready now.[/]"
        )
    if not explain:
        console.print("[dim]Deterministic review only — no code is sent to an AI service.[/]")
    console.print(center(Panel.fit(
        f"[bold]Review ready[/]  {reference.slug}#{number}\n"
        f"[dim]Mode: {'deterministic + AI explanation' if explain else 'deterministic only'} · interactive output[/]",
        border_style="green",
    )))
    console.print(center(Text.from_markup("[dim]Reading the pull request and preparing your review…\n[/]")))
    args = parser.parse_args(["pr", reference.slug, str(number)])
    args.token = token
    args.explain = explain
    args.interactive = True
    return run_pr(args)


def run_setup(args: argparse.Namespace) -> int:
    """Teach the core Diffly workflow through a short terminal walkthrough."""
    pages = [
        ("Welcome", "[bold cyan]diffly[/] turns a pull request — or your local git changes — into a deterministic review gate.\n\nRun [bold]diffly[/] with no arguments whenever you want the guided PR wizard."),
        ("Review a PR", "[bold]diffly pr OWNER/REPO NUMBER[/]\n\nPaste a full pull-request URL and the number is inferred. Add [cyan]--interactive[/] for the keyboard view, [cyan]--explain[/] for optional generated context, or [cyan]--output report.md[/] to save Markdown."),
        ("Analyze a local folder", "[bold]diffly local ~/code/my-project[/]\n\nTriage uncommitted working-tree changes — or compare a branch with [cyan]--base main[/]. Works fully offline, even for repositories that are private or no longer exist on GitHub."),
        ("Interactive controls", "[cyan]↑ / ↓[/] move between report sections\n[cyan]Space[/] enables or disables a section\n[cyan]Enter[/] renders the focused report\n[cyan]q[/] exits"),
        ("Automation", "Use [bold]diffly pr OWNER/REPO NUMBER --json[/] in scripts and CI.\n\nThe command exits 0 after successful analysis; enforce policy by reading the JSON [cyan]verdict[/] field."),
        ("Troubleshooting", "Run [bold]diffly doctor[/] to check Python, terminal support, token configuration, and PATH setup.\n\nRun [bold]diffly help[/] for the complete command list and [bold]diffly version[/] when reporting an issue."),
        ("Credentials and privacy", "Set [bold]GITHUB_TOKEN[/] for private repositories and higher API limits. Tokens are never shown by the wizard. Local mode never touches the network at all.\n\nDeterministic mode sends no code to an LLM. [cyan]--explain[/] uses your configured model endpoint."),
    ]
    for index, (title, body) in enumerate(pages, start=1):
        console.clear()
        console.print()
        console.print(center(Panel(body, title=f"[bold]{index}/{len(pages)} · {title}[/]", subtitle="[dim]Enter next · q quit[/]", border_style="cyan", padding=(1, 2))))
        choice = Prompt.ask("[dim]Press Enter to continue[/]", default="", show_default=False)
        if choice.strip().lower() == "q":
            return 0
    console.clear()
    console.print(center(Panel.fit("[bold green]Setup complete[/]\n[dim]You can rerun this guide anytime with `diffly setup`.[/]", border_style="green", padding=(1, 2))))
    if Confirm.ask("[cyan]Try the guided PR wizard now?[/]", default=True):
        return run_wizard(args.root_parser)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="diffly", description="Deterministic triage for large GitHub pull requests", formatter_class=argparse.RawDescriptionHelpFormatter, epilog="Examples:\n  diffly pr astral-sh/ruff 27808\n  diffly pr https://github.com/astral-sh/ruff/pull/27808\n  diffly pr astral-sh/ruff 27808 --interactive\n  diffly local ~/code/my-repo --base main\n  diffly doctor")
    parser.add_argument("-V", "--version", action="version", version=f"diffly {__version__}", help="Show the diffly version and exit")
    subparsers = parser.add_subparsers(dest="command", required=True)
    pr = subparsers.add_parser("pr", help="Analyze one GitHub pull request")
    pr.add_argument("repository", type=parse_repo, metavar="OWNER/REPO", help="owner/repo, a GitHub URL, or a full pull-request URL")
    pr.add_argument("number", type=positive_pr_number, nargs="?", default=None, metavar="PR-NUMBER", help="Required unless the repository argument is a pull-request URL")
    pr.add_argument("--token", default=None, help="GitHub token; defaults to GITHUB_TOKEN")
    pr.add_argument("--output", help="Write terminal Markdown to a file")
    pr.add_argument("--json", action="store_true", help="Emit structured JSON instead of Markdown")
    pr.add_argument("--explain", action="store_true", help="Add an optional LLM-generated literate-diff explanation")
    pr.add_argument("--llm-model", default=None, help="Override DIFFLY_LLM_MODEL for --explain")
    pr.add_argument("--llm-base-url", default=None, help="Override DIFFLY_LLM_BASE_URL for --explain")
    pr.add_argument("--interactive", action="store_true", help="Open a keyboard-driven report view (arrows, space, enter)")
    pr.set_defaults(func=run_pr)
    local = subparsers.add_parser("local", help="Analyze local git changes in a folder — no GitHub needed (works for private or removed repositories)")
    local.add_argument("path", nargs="?", default=".", metavar="FOLDER", help="Path to a local git repository (default: current directory)")
    local.add_argument("--base", default=None, metavar="REF", help="Compare against this git ref (e.g. main) instead of the working tree")
    local.add_argument("--output", help="Write terminal Markdown to a file")
    local.add_argument("--json", action="store_true", help="Emit structured JSON instead of Markdown")
    local.add_argument("--explain", action="store_true", help="Add an optional LLM-generated literate-diff explanation")
    local.add_argument("--llm-model", default=None, help="Override DIFFLY_LLM_MODEL for --explain")
    local.add_argument("--llm-base-url", default=None, help="Override DIFFLY_LLM_BASE_URL for --explain")
    local.add_argument("--interactive", action="store_true", help="Open a keyboard-driven report view (arrows, space, enter)")
    local.set_defaults(func=run_local)
    doctor = subparsers.add_parser("doctor", help="Diagnose local installation and environment")
    doctor.set_defaults(func=run_doctor)
    version = subparsers.add_parser("version", help="Print the installed diffly version")
    version.set_defaults(func=run_version)
    help_command = subparsers.add_parser("help", help="Show commands, options, and examples")
    help_command.set_defaults(func=run_help, root_parser=parser)
    setup = subparsers.add_parser("setup", help="Learn Diffly through a guided terminal tutorial")
    setup.set_defaults(func=run_setup, root_parser=parser)
    update_cmd = subparsers.add_parser("update", help="Check for and install the latest diffly release")
    update_cmd.set_defaults(func=run_update)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    effective_argv = sys.argv[1:] if argv is None else argv
    if not effective_argv:
        return run_wizard(parser)
    args = parser.parse_args(effective_argv)
    if args.command not in ("update", "version", "help", "doctor"):
        _check_and_prompt_update()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
