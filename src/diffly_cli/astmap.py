from __future__ import annotations

import re
from dataclasses import dataclass

from .diffparse import added_source, old_source, changed_line_numbers, deleted_line_numbers, enrich_file, language_for_path
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
    
    def walk_with_context(node, current_func=None):
        my_func = current_func
        if node.type in FUNCTION_NODES:
            my_func = _node_name(node, source)
            symbols.append(Symbol(
                name=my_func,
                start_line=node.start_point[0] + 1,
                end_line=node.end_point[0] + 1,
                kind=node.type,
            ))
        if node.type in {"call", "call_expression", "invocation_expression"} and node.children:
            # Handle member calls like service.target() by getting the terminal member name
            first = node.children[0]
            if first.type in {"member_expression", "field_expression", "property_identifier"}:
                last_child = first.children[-1] if first.children else first
                name = source[last_child.start_byte : last_child.end_byte].decode("utf-8", errors="replace")
            else:
                name = source[first.start_byte : first.end_byte].decode("utf-8", errors="replace")
            # For caller, we record the enclosing function, not just the called name
            if my_func:
                calls.append((my_func, node.start_point[0] + 1))
        for child in node.children:
            walk_with_context(child, my_func)

    walk_with_context(tree.root_node)
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
    old_source_text = old_source(file.patch)
    
    changed_lines = set(changed_line_numbers(file))
    deleted_lines = set(deleted_line_numbers(file))
    
    if not source_text.strip() and not old_source_text.strip():
        return file
        
    def get_symbols_and_calls(text):
        if not text.strip():
            return [], []
        try:
            s, c = _tree_sitter_symbols(text, language) if language else ([], [])
            if not s:
                s, c = _regex_symbols(text, language or "unknown")
            return s, c
        except Exception:
            try:
                return _regex_symbols(text, language or "unknown")
            except Exception:
                return [], []

    # Calculate actual hunk offsets properly
    # In tree-sitter we parse the whole added_source (which has no context lines, so lines don't match original file)
    # The correct fix for F-02 is to map parsed lines back to original file lines, or parse per hunk.
    # We'll parse the whole added_source but keep track of line mapping.
    
    def map_lines(text, hunk_lines_func):
        mapping = {}
        current_parsed = 1
        for hunk in file.hunks:
            if hunk_lines_func == changed_line_numbers:
                orig_line = hunk.new_start
            else:
                orig_line = hunk.old_start
                
            for line in hunk.lines:
                if line.startswith("+++") or line.startswith("---"):
                    continue
                if hunk_lines_func == changed_line_numbers and line.startswith("+"):
                    mapping[current_parsed] = orig_line
                    current_parsed += 1
                    orig_line += 1
                elif hunk_lines_func == deleted_line_numbers and line.startswith("-"):
                    mapping[current_parsed] = orig_line
                    current_parsed += 1
                    orig_line += 1
                elif line.startswith(" "):
                    mapping[current_parsed] = orig_line
                    current_parsed += 1
                    orig_line += 1
                elif hunk_lines_func == changed_line_numbers and line.startswith("-"):
                    pass
                elif hunk_lines_func == deleted_line_numbers and line.startswith("+"):
                    pass
        return mapping

    added_mapping = map_lines(source_text, changed_line_numbers)
    old_mapping = map_lines(old_source_text, deleted_line_numbers)
    
    added_symbols, added_calls = get_symbols_and_calls(source_text)
    old_symbols, _ = get_symbols_and_calls(old_source_text)
    
    touched = []
    
    for symbol in added_symbols:
        orig_start = added_mapping.get(symbol.start_line, symbol.start_line)
        orig_end = added_mapping.get(symbol.end_line, symbol.end_line)
        if any(orig_start <= line <= orig_end for line in changed_lines):
            touched.append(symbol.name)
            
    for symbol in old_symbols:
        orig_start = old_mapping.get(symbol.start_line, symbol.start_line)
        orig_end = old_mapping.get(symbol.end_line, symbol.end_line)
        if any(orig_start <= line <= orig_end for line in deleted_lines):
            touched.append(symbol.name)
            
    if not touched and (changed_lines or deleted_lines):
        touched = ["<top-level changes>"]
        
    touched_set = set(touched)
    
    callers = []
    for name, line in added_calls:
        orig_line = added_mapping.get(line, line)
        if orig_line in changed_lines:
            callers.append(name)
            
    file.touched_symbols = sorted(dict.fromkeys(touched))
    file.callers = sorted(dict.fromkeys(callers))
    return file


def analyze_files(files: list[ChangedFile]) -> list[ChangedFile]:
    return [analyze_file(file) for file in files]
