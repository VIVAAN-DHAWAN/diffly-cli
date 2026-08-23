import argparse
import json
from dataclasses import asdict

import pytest

from diffly_cli.cli import build_parser, build_result, parse_repo, run_wizard, summarize_checks
from diffly_cli.github import GitHubClient, GitHubError, RepositoryTreeResult
from diffly_cli.models import ChangedFile, PRMetadata


def metadata() -> PRMetadata:
    return PRMetadata(
        owner="acme", repo="demo", number=1, title="Test", body="", state="open", author="dev",
        base_ref="main", head_ref="feature", base_sha="base", head_sha="head", mergeable_state="clean",
        additions=1, deletions=0, changed_files=1, commits=1, html_url="https://github.com/acme/demo/pull/1",
    )


class FakePRClient:
    def __init__(self, *, diff=None, diff_error=False, tree=None):
        self.diff = diff
        self.diff_error = diff_error
        self.tree = tree or RepositoryTreeResult(["src/app.py", "tests/test_app.py"], False)

    def pull_request(self, owner, repo, number):
        return metadata()

    def pull_request_files(self, owner, repo, number):
        return [ChangedFile("src/app.py", "modified", 1, 0, 1, self.diff_patch)]

    @property
    def diff_patch(self):
        return ""

    def pull_request_diff(self, owner, repo, number):
        if self.diff_error:
            raise GitHubError("GitHub API 406: diff too large")
        return self.diff or ""

    def check_runs(self, owner, repo, ref):
        return {"check_runs": [{"name": "ci", "conclusion": "success"}], "total_count": 1}

    def commit_status(self, owner, repo, ref):
        return {"state": "success", "statuses": [], "total_count": 0}

    def repository_tree(self, owner, repo, ref):
        return self.tree


def test_large_raw_diff_failure_does_not_abort_triage():
    result = build_result(FakePRClient(diff_error=True), "acme", "demo", 1)
    assert result.metadata.repo == "demo"
    assert result.files[0].path == "src/app.py"


def test_raw_diff_enriches_file_records_when_file_patch_is_missing():
    diff = "diff --git a/src/app.py b/src/app.py\n--- a/src/app.py\n+++ b/src/app.py\n@@ -1 +1 @@\n-def old():\n+def new():\n"
    result = build_result(FakePRClient(diff=diff), "acme", "demo", 1)
    assert result.files[0].patch.startswith("diff --git a/src/app.py")
    assert "new" in result.files[0].touched_symbols
    json.dumps(asdict(result.files[0]))


def test_truncated_tree_is_quarantined_without_definitive_no_coverage_flag():
    client = FakePRClient(tree=RepositoryTreeResult(["src/app.py"], True))
    result = build_result(client, "acme", "demo", 1)
    codes = {flag.code for flag in result.flags}
    assert "REPOSITORY_TREE_INCOMPLETE" in codes
    assert "NO_TEST_COVERAGE" not in codes


def test_combined_commit_status_error_is_failure():
    checks = summarize_checks(
        {"check_runs": []},
        {"state": "error", "statuses": []},
    )
    assert checks["state"] == "failure"
    assert "combined commit status" in checks["failed"]


class PaginatedClient(GitHubClient):
    def request(self, path, *, accept="application/vnd.github+json", params=None):
        page = (params or {}).get("page", 1)
        if path.endswith("/check-runs"):
            if page == 1:
                return {"total_count": 101, "check_runs": [{"name": f"run-{i}", "conclusion": "success"} for i in range(100)]}
            return {"total_count": 101, "check_runs": [{"name": "run-100", "conclusion": "failure"}]}
        if path.endswith("/status"):
            if page == 1:
                return {"total_count": 101, "statuses": [{"context": f"status-{i}", "state": "success"} for i in range(100)]}
            return {"total_count": 101, "statuses": [{"context": "status-100", "state": "error"}]}
        raise AssertionError(path)


def test_check_and_status_endpoints_are_paginated():
    client = PaginatedClient()
    checks = client.check_runs("acme", "demo", "head")
    status = client.commit_status("acme", "demo", "head")
    assert len(checks["check_runs"]) == 101
    assert len(status["statuses"]) == 101
    assert checks["check_runs"][-1]["conclusion"] == "failure"
    assert status["statuses"][-1]["state"] == "error"


def test_repository_parser_rejects_path_and_query_injection_values():
    assert parse_repo("https://github.com/acme/demo").slug == "acme/demo"
    for value in ("acme/demo?x=1", "acme/demo#fragment", "acme/demo%2Fother", "acme/demo/extra"):
        with pytest.raises(argparse.ArgumentTypeError):
            parse_repo(value)


def test_cli_rejects_non_positive_pull_request_numbers():
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["pr", "acme/demo", "0"])
    with pytest.raises(SystemExit):
        parser.parse_args(["pr", "acme/demo", "-1"])
    with pytest.raises(SystemExit):
        parser.parse_args(["pr", "acme/demo", "1_000"])


def test_repository_parser_strips_surrounding_whitespace():
    assert parse_repo(" acme/demo ").slug == "acme/demo"
    assert parse_repo("  https://github.com/acme/demo/  ").slug == "acme/demo"


def test_repository_parser_accepts_pull_request_urls():
    reference = parse_repo("https://github.com/acme/demo/pull/42")
    assert (reference.owner, reference.repo, reference.pr_number) == ("acme", "demo", 42)
    assert parse_repo("acme/demo").pr_number is None
    with pytest.raises(argparse.ArgumentTypeError):
        parse_repo("https://github.com/acme/demo/pull/not-a-number")


def test_version_flag_prints_version_and_exits(capsys):
    from diffly_cli import __version__

    parser = build_parser()
    with pytest.raises(SystemExit) as excinfo:
        parser.parse_args(["--version"])
    assert excinfo.value.code == 0
    assert __version__ in capsys.readouterr().out


def test_zero_argument_invocation_in_non_tty_shows_help(capsys, monkeypatch):
    import diffly_cli.cli as cli

    monkeypatch.setattr(cli.sys.stdin, "isatty", lambda: False)
    assert cli.main([]) == 2
    assert "usage:" in capsys.readouterr().out


def test_pr_command_requires_number_when_repository_has_no_url_number():
    import diffly_cli.cli as cli

    parser = build_parser()
    args = parser.parse_args(["pr", "acme/demo"])
    assert args.number is None
    assert cli.run_pr(args) == 2
    args_with_url = parser.parse_args(["pr", "https://github.com/acme/demo/pull/42"])
    assert args_with_url.number is None
    assert args_with_url.repository.pr_number == 42


def test_wizard_builds_arguments_from_parser_defaults(monkeypatch):
    import diffly_cli.cli as cli

    captured: dict[str, argparse.Namespace] = {}

    def fake_run_pr(args):
        captured["args"] = args
        return 0

    monkeypatch.setattr(cli, "run_pr", fake_run_pr)
    monkeypatch.setattr(cli.sys.stdin, "isatty", lambda: True)
    monkeypatch.setattr(cli.sys.stdout, "isatty", lambda: True)
    answers = iter(["acme/demo", "42"])
    monkeypatch.setattr(cli.Prompt, "ask", staticmethod(lambda *a, **k: next(answers)))
    monkeypatch.setattr(cli.Confirm, "ask", staticmethod(lambda *a, **k: False))
    assert cli.run_wizard(build_parser()) == 0
    args = captured["args"]
    assert args.repository.slug == "acme/demo"
    assert args.number == 42
    assert args.interactive is True
    assert args.output is None
    assert args.json is False
    assert args.llm_model is None


def test_cli_exposes_interactive_and_diagnostics_commands():
    parser = build_parser()
    args = parser.parse_args(["pr", "acme/demo", "1", "--interactive"])
    assert args.interactive is True
    assert parser.parse_args(["doctor"]).command == "doctor"
    assert parser.parse_args(["version"]).command == "version"
    assert parser.parse_args(["help"]).command == "help"
    assert parser.parse_args(["setup"]).command == "setup"


def test_interactive_menu_keeps_the_generated_explanation_section():
    import diffly_cli.cli as cli
    from diffly_cli.explainer import ExplanationResult

    sections = cli.interactive_sections(ExplanationResult({"intent": "example"}, 0, "gpt-5-mini"))

    assert [key for key, _, _ in sections] == ["verdict", "checks", "risks", "files", "explain"]
    assert sections[-1][1] == "Explanation"


def test_wizard_offers_a_local_explanation_when_no_key_is_configured(monkeypatch):
    import diffly_cli.cli as cli

    captured: dict[str, argparse.Namespace] = {}
    monkeypatch.delenv("DIFFLY_LLM_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setattr(cli.sys.stdin, "isatty", lambda: True)
    monkeypatch.setattr(cli.sys.stdout, "isatty", lambda: True)
    monkeypatch.setattr(cli, "_check_and_prompt_update", lambda: None)
    monkeypatch.setattr(cli, "show_loading_screen", lambda message: None)
    answers = iter(["acme/demo", "42"])
    monkeypatch.setattr(cli.Prompt, "ask", staticmethod(lambda *a, **k: next(answers)))
    monkeypatch.setattr(cli.Confirm, "ask", staticmethod(lambda *a, **k: True))

    def fake_run_pr(args):
        captured["args"] = args
        return 0

    monkeypatch.setattr(cli, "run_pr", fake_run_pr)

    assert cli.run_wizard(build_parser()) == 0
    assert captured["args"].explain is True


def test_pr_not_found_error_explains_how_to_recover(monkeypatch):
    import diffly_cli.cli as cli
    from rich.console import Console

    recorded = Console(record=True, width=100)
    monkeypatch.setattr(cli, "console", recorded)
    cli.render_pr_error(cli.RepoRef("acme", "demo"), 42, GitHubError("GitHub API 404 for /repos/acme/demo/pulls/42"))

    output = recorded.export_text()
    assert "Pull request not found" in output
    assert "acme/demo#42" in output
    assert "paste the full pull-request URL" in output


def test_github_client_reuses_an_authenticated_gh_session(monkeypatch):
    import diffly_cli.github as github

    github.github_auth_token.cache_clear()
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)

    class Completed:
        returncode = 0
        stdout = "gho_example_token\n"

    monkeypatch.setattr(github.subprocess, "run", lambda *args, **kwargs: Completed())
    try:
        assert github.GitHubClient().token == "gho_example_token"
    finally:
        github.github_auth_token.cache_clear()


def test_zero_argument_invocation_uses_wizard(monkeypatch):
    import diffly_cli.cli as cli

    called = {}

    def fake_wizard(parser):
        called["parser"] = parser
        return 0

    monkeypatch.setattr(cli, "run_wizard", fake_wizard)
    assert cli.main([]) == 0
    assert "parser" in called


def _triage_result():
    from diffly_cli.models import TriageResult

    return TriageResult(metadata=metadata(), files=[], flags=[], verdict="PASS", reasoning=["ok"], checks={}, source="github")


def test_escape_sequence_reader_returns_arrow_codes(monkeypatch):
    import os

    import diffly_cli.cli as cli

    read_fd, write_fd = os.pipe()
    monkeypatch.setattr(cli.sys.stdin, "fileno", lambda: read_fd)
    try:
        os.write(write_fd, b"[A")
        assert cli._read_escape_sequence(0.5) == "[A"
    finally:
        os.close(read_fd)
        os.close(write_fd)


def test_escape_sequence_reader_treats_a_lone_escape_as_empty(monkeypatch):
    import os

    import diffly_cli.cli as cli

    read_fd, write_fd = os.pipe()
    monkeypatch.setattr(cli.sys.stdin, "fileno", lambda: read_fd)
    try:
        assert cli._read_escape_sequence(0.01) == ""
    finally:
        os.close(read_fd)
        os.close(write_fd)


def test_interactive_menu_handles_arrow_keys_without_crashing(monkeypatch):
    """Regression: pressing an arrow key used to raise NameError (_read_escape_sequence missing)."""
    import io
    import os
    import pty

    import diffly_cli.cli as cli

    master_fd, slave_fd = pty.openpty()
    stream = io.TextIOWrapper(os.fdopen(slave_fd, "rb", buffering=0))
    monkeypatch.setattr(cli.sys, "stdin", stream)
    monkeypatch.setattr(cli.sys.stdout, "isatty", lambda: True)
    try:
        # Down, up, then Enter: exercises both arrow branches plus the final render.
        os.write(master_fd, "\x1b[B\x1b[A\r".encode())
        cli.interactive_view(_triage_result())
    finally:
        stream.close()
        os.close(master_fd)


def test_interactive_menu_keeps_up_with_rapid_arrow_taps(monkeypatch):
    """Regression: keystrokes arriving in one packet were swallowed by the
    buffered reader, so fast arrow taps did nothing (and Enter could be eaten,
    leaving the menu stuck)."""
    import io
    import os
    import pty
    import signal

    import diffly_cli.cli as cli

    master_fd, slave_fd = pty.openpty()
    stream = io.TextIOWrapper(os.fdopen(slave_fd, "rb", buffering=0))
    monkeypatch.setattr(cli.sys.stdout, "isatty", lambda: True)
    monkeypatch.setattr(cli.sys, "stdin", stream)
    old_alarm = signal.alarm(10)
    try:
        # Down, down, up in one burst, then Enter to leave the menu.
        os.write(master_fd, "\x1b[B\x1b[B\x1b[A\r".encode())
        cli.interactive_view(_triage_result())
    finally:
        signal.alarm(0)
        stream.close()
        os.close(master_fd)


def test_menu_exits_when_stdin_reaches_eof(monkeypatch):
    """Regression: a closed input stream used to spin the redraw loop forever."""
    import io
    import os
    import pty
    import signal

    import diffly_cli.cli as cli

    master_fd, slave_fd = pty.openpty()
    stream = io.TextIOWrapper(os.fdopen(slave_fd, "rb", buffering=0))
    monkeypatch.setattr(cli.sys.stdout, "isatty", lambda: True)
    monkeypatch.setattr(cli.sys, "stdin", stream)
    old_alarm = signal.alarm(10)
    try:
        os.close(master_fd)
        cli.interactive_view(_triage_result())
    finally:
        signal.alarm(0)
        stream.close()


def test_escape_sequence_reader_consumes_exactly_one_sequence(monkeypatch):
    """Regression: the reader used to drain up to 16 bytes, so a burst like
    '↓ space ↓' lost its Space/Enter to the escape reader and the menu hung."""
    import os

    import diffly_cli.cli as cli

    read_fd, write_fd = os.pipe()
    monkeypatch.setattr(cli.sys.stdin, "fileno", lambda: read_fd)
    try:
        os.write(write_fd, b"[A\x1b[B")
        assert cli._read_escape_sequence(0.5) == "[A"
        assert os.read(read_fd, 1) == b"\x1b"  # next keystroke must be untouched
        assert cli._read_escape_sequence(0.5) == "[B"
    finally:
        os.close(read_fd)
        os.close(write_fd)


def test_setup_delegates_the_update_check_to_the_wizard(monkeypatch):
    """Regression: `diffly setup` used to run the update check twice — once in
    main() and again inside the wizard it launches — prompting back to back."""
    import diffly_cli.cli as cli

    calls: list[str] = []
    monkeypatch.setattr(cli, "_check_and_prompt_update", lambda: calls.append("check"))
    monkeypatch.setattr(cli, "run_setup", lambda args: 0)
    assert cli.main(["setup"]) == 0
    assert calls == []

    calls.clear()
    monkeypatch.setattr(cli, "run_pr", lambda args: 0)
    assert cli.main(["pr", "acme/demo", "1"]) == 0
    assert calls == ["check"]


def test_content_lines_looking_like_headers_are_still_counted():
    """Regression: added/deleted lines whose content begins with ++/-- were
    mistaken for the file's ---/+++ header lines and dropped from counts and
    scans."""
    from diffly_cli.diffparse import files_from_unified_diff

    diff = (
        "diff --git a/notes.md b/notes.md\n"
        "index 0000001..0000002 100644\n"
        "--- a/notes.md\n"
        "+++ b/notes.md\n"
        "@@ -1,3 +1,3 @@\n"
        " intro\n"
        "--- old banner\n"
        "+++ new banner\n"
        " tail\n"
    )
    file = files_from_unified_diff(diff)[0]
    assert file.additions == 1
    assert file.deletions == 1


def test_github_json_patch_without_prelude_is_counted():
    """Bare hunk bodies (GitHub files-endpoint patches) carry no @@ prelude and
    must scan unchanged."""
    from diffly_cli.diffparse import hunk_body_lines

    body = hunk_body_lines("@@ -1,2 +1,2 @@\n-context\n+replacement\n")
    assert sum(1 for line in body if line.startswith("+")) == 1
    assert sum(1 for line in body if line.startswith("-")) == 1

    bare = hunk_body_lines("+API_KEY = 'x'\n-context\n")
    assert bare[0] == "+API_KEY = 'x'"
    assert "-context" in bare


def test_truncated_diff_block_with_prelude_but_no_hunks_counts_nothing():
    from diffly_cli.diffparse import files_from_unified_diff

    diff = (
        "diff --git a/big.bin b/big.bin\n"
        "index 0000001..0000002 100644\n"
        "Binary files a/big.bin and b/big.bin differ\n"
        "--- a/big.bin\n"
        "+++ b/big.bin\n"
    )
    file = files_from_unified_diff(diff)[0]
    assert file.additions == 0
    assert file.deletions == 0


def test_secret_on_plus_prefixed_content_line_is_detected():
    """Regression: content beginning with ++ made the whole diff line look like
    the file's +++ header, hiding it from counting and the secret scan. The
    credential must be flagged; production paths block, tests/docs quarantine."""
    from diffly_cli.models import ChangedFile
    from diffly_cli.triage import compute_flags, verdict_for

    patch = (
        "diff --git a/deploy/config.py b/deploy/config.py\n"
        "--- a/deploy/config.py\n"
        "+++ b/deploy/config.py\n"
        "@@ -1,2 +1,3 @@\n"
        " intro\n"
        "+++ postgresql://admin:hunter2@db.internal.example/prod\n"
    )
    files = [ChangedFile(path="deploy/config.py", status="modified", additions=1, deletions=0, changes=1, patch=patch)]
    checks = {"state": "success", "count": 1, "repository_tree_complete": True}
    flags = compute_flags(metadata(), files, checks, ["deploy/config.py"])
    codes = {flag.code for flag in flags}
    assert "EXPOSED_SECRET" in codes
    assert files[0].additions == 1
    assert verdict_for(flags, checks)[0] == "BLOCK"


def test_dependency_detection_survives_plus_prefixed_lines():
    from diffly_cli.models import ChangedFile
    from diffly_cli.triage import _added_dependency_names

    patch = (
        "diff --git a/package.json b/package.json\n"
        "--- a/package.json\n"
        "+++ b/package.json\n"
        "@@ -1,3 +1,4 @@\n"
        " {\n"
        '+  "left-pad": "^1.3.0",\n'
        "+  // +++ see docs\n"
        '   "name": "x"\n'
        " }\n"
    )
    names = _added_dependency_names(ChangedFile(path="package.json", status="modified", additions=2, deletions=0, changes=2, patch=patch))
    assert names == ["left-pad"]
