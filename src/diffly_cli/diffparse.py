from __future__ import annotations

import re
from pathlib import PurePosixPath

from .models import ChangedFile, Hunk

_HUNK_RE = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@(?: (.*))?$")


def parse_hunks(patch: str) -> list[Hunk]:
    if not patch:
        return []
    hunks: list[Hunk] = []
    current: Hunk | None = None
    for line in patch.splitlines():
        match = _HUNK_RE.match(line)
        if match:
            if current:
                hunks.append(current)
            old_start, old_count, new_start, new_count, _ = match.groups()
            current = Hunk(
                header=line,
                old_start=int(old_start),
                old_count=int(old_count or 1),
                new_start=int(new_start),
                new_count=int(new_count or 1),
            )
        elif current is not None:
            current.lines.append(line)
    if current:
        hunks.append(current)
    return hunks


def files_from_unified_diff(diff: str) -> list[ChangedFile]:
    """Build ChangedFile objects from a raw GitHub unified diff."""
    blocks = re.split(r"(?=^diff --git a/)", diff, flags=re.MULTILINE)
    files: list[ChangedFile] = []
    for block in blocks:
        header = re.search(r"^diff --git a/(.*?) b/(.*?)$", block, flags=re.MULTILINE)
        if not header:
            continue
        old_path, new_path = header.groups()
        path = new_path if new_path != "/dev/null" else old_path
        status = "modified"
        if re.search(r"^new file mode ", block, flags=re.MULTILINE):
            status = "added"
        elif re.search(r"^deleted file mode ", block, flags=re.MULTILINE):
            status = "removed"
        elif re.search(r"^rename from ", block, flags=re.MULTILINE):
            status = "renamed"
        additions = sum(1 for line in block.splitlines() if line.startswith("+") and not line.startswith("+++") )
        deletions = sum(1 for line in block.splitlines() if line.startswith("-") and not line.startswith("---") )
        file = ChangedFile(path=path, status=status, additions=additions, deletions=deletions, changes=additions + deletions, patch=block)
        file.hunks = parse_hunks(block)
        files.append(file)
    return files


def enrich_file(file: ChangedFile) -> ChangedFile:
    file.hunks = parse_hunks(file.patch)
    return file


def language_for_path(path: str) -> str | None:
    suffix = PurePosixPath(path).suffix.lower()
    names = {
        ".py": "python",
        ".js": "javascript",
        ".jsx": "javascript",
        ".ts": "typescript",
        ".tsx": "tsx",
        ".go": "go",
        ".java": "java",
        ".rb": "ruby",
        ".rs": "rust",
        ".c": "c",
        ".h": "c",
        ".cc": "cpp",
        ".cpp": "cpp",
        ".cs": "c_sharp",
        ".php": "php",
        ".swift": "swift",
        ".kt": "kotlin",
    }
    return names.get(suffix)


def old_source(patch: str) -> str:
    lines = []
    for line in patch.splitlines():
        if line.startswith("+++") or line.startswith("---"):
            continue
        if line.startswith("-"):
            lines.append(line[1:])
        elif line.startswith(" "):
            lines.append(line[1:])
    return "\n".join(lines)

def added_source(patch: str) -> str:
    lines = []
    for line in patch.splitlines():
        if line.startswith("+++") or line.startswith("---"):
            continue
        if line.startswith("+"):
            lines.append(line[1:])
        elif line.startswith(" "):
            lines.append(line[1:])
    return "\n".join(lines)


def changed_line_numbers(file: ChangedFile) -> list[int]:
    numbers: list[int] = []
    for hunk in file.hunks:
        line_no = hunk.new_start
        for line in hunk.lines:
            if line.startswith("+"):
                numbers.append(line_no)
                line_no += 1
            elif line.startswith("-"):
                continue
            else:
                line_no += 1
    return numbers

def deleted_line_numbers(file: ChangedFile) -> list[int]:
    numbers: list[int] = []
    for hunk in file.hunks:
        line_no = hunk.old_start
        for line in hunk.lines:
            if line.startswith("-"):
                numbers.append(line_no)
                line_no += 1
            elif line.startswith("+"):
                continue
            else:
                line_no += 1
    return numbers
