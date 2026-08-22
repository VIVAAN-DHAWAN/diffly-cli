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


def test_wizard_skips_the_ai_question_when_no_key_is_configured(monkeypatch):
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
    monkeypatch.setattr(cli.Confirm, "ask", staticmethod(lambda *a, **k: False))

    def fake_run_pr(args):
        captured["args"] = args
        return 0

    monkeypatch.setattr(cli, "run_pr", fake_run_pr)

    assert cli.run_wizard(build_parser()) == 0
    assert captured["args"].explain is False


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


def test_zero_argument_invocation_uses_wizard(monkeypatch):
    import diffly_cli.cli as cli

    called = {}

    def fake_wizard(parser):
        called["parser"] = parser
        return 0

    monkeypatch.setattr(cli, "run_wizard", fake_wizard)
    assert cli.main([]) == 0
    assert "parser" in called
