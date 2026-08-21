from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).parents[1]
FORMATTER = ROOT / "action" / "format_comment.py"
POST_COMMENT_PATH = ROOT / "action" / "post_comment.py"
_spec = importlib.util.spec_from_file_location("diffly_post_comment", POST_COMMENT_PATH)
assert _spec and _spec.loader
post_comment = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(post_comment)


def test_action_comment_contains_verdict_risk_and_collapsible_blast_radius(tmp_path: Path) -> None:
    payload = {
        "metadata": {
            "owner": "owner",
            "repo": "repo",
            "number": 7,
            "additions": 4,
            "deletions": 2,
            "changed_files": 1,
        },
        "verdict": "BLOCK",
        "reasoning": ["a check failed"],
        "checks": {"state": "failure"},
        "flags": [{"code": "CHECKS_FAILED", "severity": "critical", "message": "failure", "evidence": ["CI"]}],
        "files": [{"path": "src/app.py", "additions": 4, "deletions": 2, "touched_symbols": ["main"], "callers": [], "tests_found": []}],
    }
    input_path = tmp_path / "result.json"
    input_path.write_text(json.dumps(payload))
    completed = subprocess.run([sys.executable, str(FORMATTER), str(input_path)], check=True, capture_output=True, text=True)
    output = completed.stdout
    assert "<!-- diffly-cli:pr-triage -->" in output
    assert "**BLOCK**" in output
    assert "`CHECKS_FAILED` (critical)" in output
    assert "<summary>Blast-radius summary</summary>" in output
    assert "`src/app.py`" in output


def test_commenter_patches_existing_marked_comment(tmp_path: Path, monkeypatch) -> None:
    comment = tmp_path / "comment.md"
    comment.write_text("<!-- diffly-cli:pr-triage -->\nnew body")
    calls = []

    def fake_request(url, token, method="GET", payload=None):
        calls.append((url, method, payload))
        if method == "GET":
            return [{"id": 123, "body": "<!-- diffly-cli:pr-triage -->\nold body"}]
        return {}

    monkeypatch.setattr(post_comment, "request", fake_request)
    monkeypatch.setenv("GITHUB_TOKEN", "masked")
    monkeypatch.setattr(sys, "argv", ["post_comment.py", "owner/repo", "7", str(comment)])
    assert post_comment.main() == 0
    assert calls[-1][0].endswith("/issues/7/comments/123")
    assert calls[-1][1] == "PATCH"
    assert calls[-1][2] == {"body": "<!-- diffly-cli:pr-triage -->\nnew body"}


def test_commenter_warns_instead_of_failing_on_publish_404(tmp_path: Path, monkeypatch, capsys) -> None:
    comment = tmp_path / "comment.md"
    comment.write_text("body")

    def fake_request(url, token, method="GET", payload=None):
        if method == "GET":
            return []
        raise post_comment.GitHubApiError(404, "Not Found")

    monkeypatch.setattr(post_comment, "request", fake_request)
    monkeypatch.setenv("GITHUB_TOKEN", "masked")
    monkeypatch.setattr(sys, "argv", ["post_comment.py", "owner/repo", "7", str(comment)])
    assert post_comment.main() == 0
    assert "Warning" in capsys.readouterr().out


def test_commenter_still_fails_on_unexpected_api_errors(tmp_path: Path, monkeypatch) -> None:
    comment = tmp_path / "comment.md"
    comment.write_text("body")

    def fake_request(url, token, method="GET", payload=None):
        if method == "GET":
            return []
        raise post_comment.GitHubApiError(502, "Bad gateway")

    monkeypatch.setattr(post_comment, "request", fake_request)
    monkeypatch.setenv("GITHUB_TOKEN", "masked")
    monkeypatch.setattr(sys, "argv", ["post_comment.py", "owner/repo", "7", str(comment)])
    with pytest.raises(post_comment.GitHubApiError):
        post_comment.main()


def test_comment_listing_404_is_treated_as_no_comments(tmp_path: Path, monkeypatch) -> None:
    calls = []

    def fake_request(url, token, method="GET", payload=None):
        calls.append(url)
        if page_of(url) == 1:
            raise post_comment.GitHubApiError(404, "Not Found")
        raise AssertionError("should not paginate after a listing 404")

    def page_of(url: str) -> int:
        return int(url.rsplit("page=", 1)[1])

    monkeypatch.setattr(post_comment, "request", fake_request)
    assert post_comment.existing_comments("https://api.github.com/repos/o/r/issues/1/comments", "t") == []
