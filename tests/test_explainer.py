from diffly_cli.explainer import ExplanationResult, build_context, generate_explanation, validate_explanation
from diffly_cli.models import ChangedFile, PRMetadata, RiskFlag, TriageResult
from diffly_cli.redact import redact_secrets


class FakeClient:
    def __init__(self, payload: str):
        self.payload = payload
        self.calls = []

    def chat(self, **kwargs):
        self.calls.append(kwargs)
        return self.payload


def result(body: str = "") -> TriageResult:
    metadata = PRMetadata(
        owner="acme", repo="demo", number=1, title="Improve flow", body=body, state="open", author="dev",
        base_ref="main", head_ref="feature", base_sha="base", head_sha="head", mergeable_state="clean",
        additions=2, deletions=1, changed_files=1, commits=1, html_url="https://github.com/acme/demo/pull/1",
    )
    file = ChangedFile("src/flow.py", "modified", 2, 1, 3, "@@ -1 +1,2 @@\n+token = 'ghp_abcdefghijklmnopqrstuvwxyz123456'\n+def run():\n")
    return TriageResult(metadata, [file], [RiskFlag("NO_TEST_COVERAGE", "medium", "No obvious test", [file.path])], "QUARANTINE", ["test reason"], {"state": "success", "count": 1}, "test")


def valid_payload():
    return {
        "background": "The change updates a request flow.",
        "intent": "The author appears to make the flow easier to reuse.",
        "narrative": [{
            "title": "Introduce the new flow",
            "files": ["src/flow.py"],
            "explanation": "A new entry point is added.",
            "evidence": ["src/flow.py defines run"],
            "snippet": "def run(): ...",
        }],
        "review_questions": ["Is the new entry point covered by tests?"],
        "uncertainties": [],
    }


def test_redacts_common_secret_forms():
    raw = "Authorization: Bearer abcdefghijklmnop1234\nkey=ghp_abcdefghijklmnopqrstuvwxyz123456\n-----BEGIN PRIVATE KEY-----\nsecret\n-----END PRIVATE KEY-----"
    redacted = redact_secrets(raw)
    assert redacted.count >= 3
    assert "ghp_" not in redacted.text
    assert "BEGIN PRIVATE KEY" not in redacted.text
    assert "Bearer abc" not in redacted.text


def test_context_redacts_pr_body_and_patch():
    triage = result("password='super-secret-value'")
    context, count = build_context(triage)
    assert count >= 2
    assert "super-secret-value" not in context
    assert "ghp_" not in context
    assert "[REDACTED_SECRET]" in context or "[REDACTED_GITHUB_TOKEN]" in context


def test_strict_validation_rejects_unknown_file_citations():
    payload = valid_payload()
    payload["narrative"][0]["files"] = ["src/not-changed.py"]
    try:
        validate_explanation(payload, {"src/flow.py"})
    except ValueError:
        pass
    else:
        raise AssertionError("unknown file citations must be rejected")


def test_strict_validation_rejects_extra_keys():
    payload = valid_payload()
    payload["extra"] = "nope"
    try:
        validate_explanation(payload)
    except ValueError:
        pass
    else:
        raise AssertionError("extra keys must be rejected")


def test_fake_model_receives_schema_and_preserves_verdict():
    fake = FakeClient(__import__("json").dumps(valid_payload()))
    triage = result()
    explanation = generate_explanation(triage, client=fake, model="gpt-5-mini")
    assert explanation.error is None
    assert explanation.explanation["intent"]
    assert triage.verdict == "QUARANTINE"
    assert fake.calls[0]["token_limit_key"] == "max_completion_tokens"
    assert fake.calls[0]["response_format"]["json_schema"]["strict"] is True
    prompt = fake.calls[0]["messages"][1]["content"]
    assert "ghp_" not in prompt
    assert "[REDACTED_GITHUB_TOKEN]" in prompt or "[REDACTED_SECRET]" in prompt


def test_claude_model_uses_max_tokens():
    fake = FakeClient(__import__("json").dumps(valid_payload()))
    explanation = generate_explanation(result(), client=fake, model="claude-sonnet-4-6")
    assert explanation.error is None
    assert fake.calls[0]["token_limit_key"] == "max_tokens"


def test_model_output_is_redacted_before_validation():
    payload = valid_payload()
    payload["background"] = "The token=ghp_abcdefghijklmnopqrstuvwxyz123456 is not relevant."
    fake = FakeClient(__import__("json").dumps(payload))
    explanation = generate_explanation(result(), client=fake)
    assert explanation.error is None
    assert "ghp_" not in explanation.explanation["background"]
    assert explanation.redactions >= 1


def test_no_key_falls_back_without_calling_model(monkeypatch):
    monkeypatch.delenv("DIFFLY_LLM_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    explanation = generate_explanation(result())
    assert explanation.explanation is None
    assert "No LLM API key configured" in explanation.error


def test_model_failure_is_safe():
    fake = FakeClient("not json")
    explanation = generate_explanation(result(), client=fake)
    assert explanation.explanation is None
    assert "failed safely" in explanation.error
