from __future__ import annotations

import re
from dataclasses import dataclass

from .diffparse import added_source, changed_line_numbers, enrich_file, language_for_path
from .models import ChangedFile


@dataclass
class Symbol:
    name: str
    start_line: int
    end_line: int
    kind: str


FUNCTION_NODES = {
    "function_definition",
    "function_declaration",
    "method_definition",
    "method_declaration",
    "function_item",
    "function_expression",
    "arrow_function",
    "function",
    "method",
}


def _node_name(node, source: bytes) -> str:
    for child in node.children:
        if child.type in {"identifier", "property_identifier", "type_identifier", "name"}:
            return source[child.start_byte : child.end_byte].decode("utf-8", errors="replace")
    return node.type


def _walk(node):
    yield node
    for child in node.children:
        yield from _walk(child)


def _tree_sitter_symbols(source_text: str, language: str) -> tuple[list[Symbol], list[tuple[str, int]]]:
    from tree_sitter_language_pack import get_parser

    source = source_text.encode("utf-8")
    parser = get_parser(language)
    tree = parser.parse(source)
    symbols: list[Symbol] = []
    calls: list[tuple[str, int]] = []
    for node in _walk(tree.root_node):
        if node.type in FUNCTION_NODES:
            symbols.append(Symbol(
                name=_node_name(node, source),
                start_line=node.start_point[0] + 1,
                end_line=node.end_point[0] + 1,
                kind=node.type,
            ))
        if node.type in {"call", "call_expression", "invocation_expression", "call_expression"} and node.children:
            first = node.children[0]
            name = source[first.start_byte : first.end_byte].decode("utf-8", errors="replace")
            calls.append((name, node.start_point[0] + 1))
    return symbols, calls


def _regex_symbols(source_text: str, language: str) -> tuple[list[Symbol], list[tuple[str, int]]]:
    symbols: list[Symbol] = []
    calls: list[tuple[str, int]] = []
    patterns = [
        r"^\s*(?:async\s+)?def\s+([A-Za-z_][\w]*)\s*\(",
        r"^\s*(?:export\s+)?(?:async\s+)?function\s+([A-Za-z_][\w]*)\s*\(",
        r"^\s*(?:public|private|protected|static|async|func|fn|function|def|void|int|string|bool|var|let|const|\w+\s+)+([A-Za-z_][\w]*)\s*\([^;]*\)\s*[{:]?",
    ]
    starts: list[tuple[str, int]] = []
    lines = source_text.splitlines()
    for index, line in enumerate(lines, start=1):
        for pattern in patterns:
            match = re.match(pattern, line)
            if match:
                name = match.group(1)
                if name not in {"if", "for", "while", "switch", "catch"}:
                    starts.append((name, index))
                    break
        for match in re.finditer(r"\b([A-Za-z_][\w]*)\s*\(", line):
            if match.group(1) not in {"if", "for", "while", "switch", "catch", "def", "function"}:
                calls.append((match.group(1), index))
    for i, (name, start) in enumerate(starts):
        end = starts[i + 1][1] - 1 if i + 1 < len(starts) else len(lines)
        symbols.append(Symbol(name, start, end, "regex-definition"))
    return symbols, calls


def analyze_file(file: ChangedFile) -> ChangedFile:
    enrich_file(file)
    language = language_for_path(file.path)
    source_text = added_source(file.patch)
    changed_lines = set(changed_line_numbers(file))
    if not source_text.strip():
        return file
    try:
        symbols, calls = _tree_sitter_symbols(source_text, language) if language else ([], [])
    except Exception:
        symbols, calls = _regex_symbols(source_text, language or "unknown")
    if not symbols:
        try:
            symbols, calls = _regex_symbols(source_text, language or "unknown")
        except Exception:
            symbols, calls = [], []
    touched = [symbol.name for symbol in symbols if any(symbol.start_line <= line <= symbol.end_line for line in changed_lines)]
    if not touched and changed_lines:
        touched = ["<top-level changes>"]
    touched_set = set(touched)
    callers = [name for name, _ in calls if name in touched_set]
    file.touched_symbols = sorted(dict.fromkeys(touched))
    file.callers = sorted(dict.fromkeys(callers))
    return file


def analyze_files(files: list[ChangedFile]) -> list[ChangedFile]:
    return [analyze_file(file) for file in files]
