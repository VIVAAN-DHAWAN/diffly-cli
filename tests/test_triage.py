from diffly_cli.diffparse import parse_hunks
from diffly_cli.models import ChangedFile, PRMetadata
from diffly_cli.triage import compute_flags, verdict_for


def metadata() -> PRMetadata:
    return PRMetadata(
        owner="acme", repo="demo", number=1, title="Test", body="", state="open", author="dev",
        base_ref="main", head_ref="feature", base_sha="base", head_sha="head", mergeable_state="clean",
        additions=1, deletions=0, changed_files=1, commits=1, html_url="https://example.com",
    )


def test_parse_hunks_tracks_ranges_and_lines():
    hunks = parse_hunks("@@ -1,2 +1,3 @@ def hello\n old\n-old\n+new\n+extra\n")
    assert len(hunks) == 1
    assert hunks[0].new_start == 1
    assert hunks[0].new_count == 3
    assert "+new" in hunks[0].lines


def test_auth_change_blocks():
    file = ChangedFile("src/auth.py", "modified", 1, 0, 1, "+def login():\n")
    flags = compute_flags(metadata(), [file], {"state": "success", "count": 1}, ["src/auth.py", "tests/test_auth.py"])
    verdict, _ = verdict_for(flags, {"state": "success"})
    assert "AUTH_OR_SECRET" in {flag.code for flag in flags}
    assert verdict == "BLOCK"


def test_dependency_and_missing_tests_quarantines():
    files = [
        ChangedFile("pyproject.toml", "modified", 1, 0, 1, '+dependencies = ["new-lib"]\n'),
        ChangedFile("src/new_module.py", "added", 3, 0, 3, "+def run():\n+    return 1\n"),
    ]
    flags = compute_flags(metadata(), files, {"state": "success", "count": 1}, ["pyproject.toml", "src/new_module.py"])
    verdict, _ = verdict_for(flags, {"state": "success"})
    assert "NEW_DEPENDENCY" in {flag.code for flag in flags}
    assert "NO_TEST_COVERAGE" in {flag.code for flag in flags}
    assert verdict == "QUARANTINE"


def test_all_clear_ships():
    file = ChangedFile("tests/test_math.py", "modified", 1, 0, 1, "+def test_math():\n")
    flags = compute_flags(metadata(), [file], {"state": "success", "count": 1}, ["tests/test_math.py"])
    verdict, _ = verdict_for(flags, {"state": "success"})
    assert not flags
    assert verdict == "PASS"


def test_pending_checks_quarantine():
    flags = compute_flags(metadata(), [], {"state": "pending", "count": 1}, [])
    verdict, reasoning = verdict_for(flags, {"state": "pending"})
    assert "CHECKS_PENDING" in {flag.code for flag in flags}
    assert verdict == "QUARANTINE"
    assert any("still running" in item for item in reasoning)
