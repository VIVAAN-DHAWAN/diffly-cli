from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class PRMetadata:
    owner: str
    repo: str
    number: int
    title: str
    body: str
    state: str
    author: str
    base_ref: str
    head_ref: str
    base_sha: str
    head_sha: str
    mergeable_state: str
    additions: int
    deletions: int
    changed_files: int
    commits: int
    html_url: str


@dataclass
class Hunk:
    header: str
    old_start: int
    old_count: int
    new_start: int
    new_count: int
    lines: list[str] = field(default_factory=list)


@dataclass
class ChangedFile:
    path: str
    status: str
    additions: int
    deletions: int
    changes: int
    patch: str = ""
    hunks: list[Hunk] = field(default_factory=list)
    touched_symbols: list[str] = field(default_factory=list)
    callers: list[str] = field(default_factory=list)
    tests_found: list[str] = field(default_factory=list)


@dataclass
class RiskFlag:
    code: str
    severity: str
    message: str
    evidence: list[str] = field(default_factory=list)


@dataclass
class TriageResult:
    metadata: PRMetadata
    files: list[ChangedFile]
    flags: list[RiskFlag]
    verdict: str
    reasoning: list[str]
    checks: dict[str, Any]
    source: str
