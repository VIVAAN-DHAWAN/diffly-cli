import pytest
from diffly_cli.cli import build_parser, run_pr
from diffly_cli.diffparse import files_from_unified_diff
from diffly_cli.astmap import analyze_files
from diffly_cli.triage import _matches, _covered_by_test, _is_production_file
from diffly_cli.models import ChangedFile
from diffly_cli.redact import redact_secrets

def test_hunk_offsets_and_deletion():
    diff = """diff --git a/src/app.py b/src/app.py
--- a/src/app.py
+++ b/src/app.py
@@ -99,2 +99,3 @@
 def existing():
     pass
+def added_func():
+    pass
@@ -200,3 +201,0 @@
-def removed_func():
-    pass
"""
    files = files_from_unified_diff(diff)
    files = analyze_files(files)
    file = files[0]
    
    assert "added_func" in file.touched_symbols
    assert "removed_func" in file.touched_symbols
    assert "<top-level changes>" not in file.touched_symbols

def test_member_call():
    diff = """diff --git a/src/app.py b/src/app.py
--- a/src/app.py
+++ b/src/app.py
@@ -10,0 +11,3 @@
+def caller_func():
+    service.target()
+    target()
"""
    files = files_from_unified_diff(diff)
    files = analyze_files(files)
    file = files[0]
    
    assert "caller_func" in file.touched_symbols
    assert "caller_func" in file.callers

def test_policy_precision():
    assert _is_production_file("src/token.py") == True
    assert _is_production_file("docs/security.md") == False
    assert _is_production_file("tests/test_token.py") == False
    
    # Exact coverage matching
    file = ChangedFile("src/foo.py", "modified", 1, 0, 1, "")
    assert _covered_by_test(file, ["tests/test_foo_unrelated.py"]) == []
    assert _covered_by_test(file, ["tests/test_foo.py"]) == ["tests/test_foo.py"]
    
    # Check that test_cli.py covers cli.py
    file_cli = ChangedFile("src/diffly_cli/cli.py", "modified", 1, 0, 1, "")
    assert _covered_by_test(file_cli, ["tests/test_cli.py"]) == ["tests/test_cli.py"]

def test_redaction_expansion():
    text = "aws AWS_SECRET_ACCESS_KEY='AKIAIOSFODNN7EXAMPLE12345678901234567890'"
    res = redact_secrets(text)
    assert "[REDACTED_AWS_SECRET_KEY]" in res.text
    assert "AKIAIOSFODNN7EXAMPLE" not in res.text
    
    text = "slack xoxb-12345678901-12345678901-abcdefg12345"
    res = redact_secrets(text)
    assert "[REDACTED_SLACK_TOKEN]" in res.text
    assert "xoxb" not in res.text
    
    text = '{"clientSecret": "super_secret_value"}'
    res = redact_secrets(text)
    assert "[REDACTED_SECRET]" in res.text
    assert "super_secret_value" not in res.text
