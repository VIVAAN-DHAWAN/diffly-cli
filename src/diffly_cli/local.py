"""Local-mode triage: analyze git changes in a folder without GitHub.

Useful when the repository is private, archived, or has been removed from its
host — anyone with a clone (or a downloaded snapshot containing `.git`) can
still run the full deterministic risk pass entirely on their machine.
"""
from __future__ import annotations

import getpass
import subprocess
from pathlib import Path

from .astmap import analyze_files
from .diffparse import files_from_unified_diff
from .models import ChangedFile, PRMetadata, TriageResult
from .triage import compute_flags, verdict_for

MAX_UNTRACKED_PATCH_LINES = 4_000
MAX_REPO_PATHS = 50_000


class LocalAnalysisError(RuntimeError):
    """Raised when a folder cannot be analyzed as a git repository."""


def _git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
        timeout=60,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or f"exit code {completed.returncode}"
        raise LocalAnalysisError(f"git {' '.join(args)} failed: {detail}")
    return completed.stdout


def resolve_repository_root(raw_path: str) -> Path:
    root = Path(raw_path).expanduser().resolve()
    if not root.exists():
        raise LocalAnalysisError(f"path does not exist: {root}")
    completed = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise LocalAnalysisError(
            f"{root} is not inside a git repository; local analysis needs git history to produce a diff."
        )
    return Path(completed.stdout.strip())


def _current_branch(root: Path) -> str:
    try:
        return _git(root, "rev-parse", "--abbrev-ref", "HEAD").strip() or "HEAD"
    except LocalAnalysisError:
        return "HEAD"


def _unified_diff(root: Path, base: str | None) -> str:
    if base:
        return _git(root, "diff", f"{base}...HEAD")
    return _git(root, "diff", "HEAD")


def _untracked_paths(root: Path) -> list[str]:
    return [line for line in _git(root, "ls-files", "--others", "--exclude-standard").splitlines() if line.strip()]


def _untracked_file_entries(root: Path, paths: list[str]) -> list[ChangedFile]:
    entries: list[ChangedFile] = []
    for relative in paths:
        try:
            text = (root / relative).read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        lines = text.splitlines()
        shown = lines[:MAX_UNTRACKED_PATCH_LINES]
        patch = "\n".join([
            f"diff --git a/{relative} b/{relative}",
            "--- /dev/null",
            f"+++ b/{relative}",
            f"@@ -0,0 +1,{len(shown)} @@",
            *(f"+{line}" for line in shown),
        ])
        entries.append(ChangedFile(path=relative, status="added", additions=len(lines), deletions=0, changes=len(lines), patch=patch))
    return entries


def _repository_paths(root: Path) -> list[str]:
    listing = _git(root, "ls-files", "-co", "--exclude-standard").splitlines()
    return listing[:MAX_REPO_PATHS]


def build_local_result(raw_path: str = ".", base: str | None = None) -> TriageResult:
    """Run the same deterministic pipeline over local git changes."""
    root = resolve_repository_root(raw_path)
    branch = _current_branch(root)
    diff = _unified_diff(root, base)
    files = files_from_unified_diff(diff)
    untracked = _untracked_file_entries(root, _untracked_paths(root))
    files.extend(untracked)
    # A clean tree is a valid result: zero files, zero flags, PASS.
    files = analyze_files(files)

    head_sha = "worktree"
    try:
        head_sha = _git(root, "rev-parse", "HEAD").strip()[:12]
    except LocalAnalysisError:
        pass
    commits = 1
    if base:
        commits = int(_git(root, "rev-list", "--count", f"{base}..HEAD").strip() or 1)
    metadata = PRMetadata(
        owner="local",
        repo=root.name,
        number=0,
        title=f"Local changes on {branch}" + (f" vs {base}" if base else ""),
        body="",
        state="local",
        author=_git_author(root),
        base_ref=base or "worktree",
        head_ref=branch,
        base_sha="",
        head_sha=head_sha,
        mergeable_state="local",
        additions=sum(file.additions for file in files),
        deletions=sum(file.deletions for file in files),
        changed_files=len(files),
        commits=commits,
        html_url=f"file://{root}",
    )
    repo_paths = _repository_paths(root)
    checks = {"state": "not_applicable", "count": 0, "repository_tree_complete": True}
    flags = compute_flags(metadata, files, checks, repo_paths)
    verdict, reasoning = verdict_for(flags, checks)
    source = f"Local git ({f'vs {base}' if base else 'working tree'})"
    return TriageResult(metadata, files, flags, verdict, reasoning, checks, source)


def _git_author(root: Path) -> str:
    for args in (("config", "user.name"), ("log", "-1", "--pretty=%an")):
        try:
            name = _git(root, *args).strip()
            if name:
                return name
        except LocalAnalysisError:
            continue
    return getpass.getuser() or "unknown"
