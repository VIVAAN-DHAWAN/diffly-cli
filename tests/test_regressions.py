import argparse
import json
from dataclasses import asdict

import pytest

from diffly_cli.cli import build_result, parse_repo, summarize_checks
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
    assert parse_repo("https://github.com/acme/demo") == ("acme", "demo")
    for value in ("acme/demo?x=1", "acme/demo#fragment", "acme/demo%2Fother", "acme/demo/extra"):
        with pytest.raises(argparse.ArgumentTypeError):
            parse_repo(value)
