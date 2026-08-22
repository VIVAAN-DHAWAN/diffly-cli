from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from diffly_cli.cli import render_markdown
from diffly_cli.local import LocalAnalysisError, build_local_result, resolve_repository_root
from diffly_cli.models import TriageResult
from diffly_cli.triage import compute_flags, verdict_for


def _git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(root), "-c", "user.email=diffly@test", "-c", "user.name=Diffly Test", *args],
        capture_output=True,
        text=True,
        check=True,
    )
    return completed.stdout


@pytest.fixture()
def repo(tmp_path: Path) -> Path:
    root = tmp_path / "sample"
    root.mkdir()
    _git(root, "init", "-q", "-b", "main")
    (root / "src").mkdir()
    (root / "tests").mkdir()
    (root / "src" / "app.py").write_text("def hello():\n    return 'hi'\n")
    (root / "tests" / "test_app.py").write_text("from src.app import hello\n\ndef test_hello():\n    assert hello()\n")
    _git(root, "add", ".")
    _git(root, "commit", "-qm", "initial")
    return root


def test_clean_tree_passes_locally(repo: Path) -> None:
    result = build_local_result(str(repo))
    assert isinstance(result, TriageResult)
    assert not result.flags
    assert result.verdict == "PASS"
    assert any("no CI checks" in reason for reason in result.reasoning)
    assert result.source.startswith("Local git")


def test_working_tree_change_without_tests_passes_with_a_review_note(repo: Path) -> None:
    (repo / "src" / "orphan_module.py").write_text("def lonely():\n    return 1\n")
    result = build_local_result(str(repo))
    codes = {flag.code for flag in result.flags}
    assert "NO_TEST_COVERAGE" in codes
    assert result.verdict == "PASS"
    assert result.metadata.changed_files == 1


def test_untracked_files_are_included(repo: Path) -> None:
    (repo / "src" / "brand_new.py").write_text("def fresh():\n    return True\n")
    result = build_local_result(str(repo))
    paths = {file.path for file in result.files}
    assert "src/brand_new.py" in paths
    new_file = next(file for file in result.files if file.path == "src/brand_new.py")
    assert new_file.status == "added"
    assert new_file.touched_symbols == ["fresh"]


def test_auth_change_quarantines_locally(repo: Path) -> None:
    (repo / "src" / "credentials.py").write_text("TOKEN = 'value'\n")
    result = build_local_result(str(repo))
    codes = {flag.code for flag in result.flags}
    assert "AUTH_OR_SECRET" in codes
    assert result.verdict == "QUARANTINE"


def test_base_ref_compares_branch_commits_only(repo: Path) -> None:
    _git(repo, "checkout", "-qb", "feature")
    (repo / "src" / "feature_module.py").write_text("def feature():\n    return 42\n")
    _git(repo, "add", ".")
    _git(repo, "commit", "-qm", "add feature")
    result = build_local_result(str(repo), base="main")
    paths = {file.path for file in result.files}
    assert "src/feature_module.py" in paths
    assert result.metadata.commits == 1
    assert "vs main" in result.source
    # The untouched committed app.py must NOT appear in a vs-main diff.
    assert "tests/test_app.py" not in paths


def test_not_applicable_checks_produce_no_check_flags() -> None:
    flags = compute_flags(
        __import__("diffly_cli.models", fromlist=["PRMetadata"]).PRMetadata(
            owner="local", repo="x", number=0, title="", body="", state="local",
            author="a", base_ref="", head_ref="", base_sha="", head_sha="",
            mergeable_state="local", additions=0, deletions=0, changed_files=0,
            commits=0, html_url="",
        ),
        [],
        {"state": "not_applicable"},
    )
    assert not {flag.code for flag in flags} & {"CHECKS_FAILED", "CHECKS_PENDING", "CHECKS_UNKNOWN"}
    verdict, reasoning = verdict_for(flags, {"state": "not_applicable"})
    assert verdict == "PASS"
    assert any("local analysis" in item for item in reasoning)


def test_non_git_folder_is_rejected(tmp_path: Path) -> None:
    plain = tmp_path / "plain"
    plain.mkdir()
    with pytest.raises(LocalAnalysisError):
        build_local_result(str(plain))
    with pytest.raises(LocalAnalysisError):
        resolve_repository_root(str(tmp_path / "missing"))


def test_repo_with_no_changes_reports_clean_pass(repo: Path) -> None:
    result = build_local_result(str(repo))
    assert result.verdict == "PASS"
    assert result.files == []
    assert result.metadata.changed_files == 0
    assert "No deterministic risk flags fired." in render_markdown(result)


def test_cli_local_command_parses():
    from diffly_cli.cli import build_parser

    parser = build_parser()
    args = parser.parse_args(["local"])
    assert args.path == "."
    assert args.base is None
    args = parser.parse_args(["local", "/tmp/somewhere", "--base", "develop", "--json"])
    assert args.path == "/tmp/somewhere"
    assert args.base == "develop"
    assert args.json is True


def test_cli_local_rejects_non_git_folder(capsys, tmp_path):
    from diffly_cli.cli import build_parser, run_local

    parser = build_parser()
    args = parser.parse_args(["local", str(tmp_path)])
    assert run_local(args) == 2
    assert "Cannot analyze folder" in capsys.readouterr().out
