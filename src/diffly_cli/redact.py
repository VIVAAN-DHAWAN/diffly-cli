from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class RedactionResult:
    text: str
    count: int
    labels: tuple[str, ...]


_PATTERNS: tuple[tuple[str, re.Pattern[str], str], ...] = (
    (
        "private_key",
        re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----.*?-----END [A-Z0-9 ]*PRIVATE KEY-----", re.DOTALL),
        "[REDACTED_PRIVATE_KEY]",
    ),
    (
        "github_token",
        re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9_\-]{20,}|github_pat_[A-Za-z0-9_\-]{20,})\b"),
        "[REDACTED_GITHUB_TOKEN]",
    ),
    (
        "aws_access_key",
        re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
        "[REDACTED_AWS_ACCESS_KEY]",
    ),
    (
        "bearer_token",
        re.compile(r"(?i)(\bBearer\s+)[A-Za-z0-9_\-.=+/]{16,}"),
        r"\1[REDACTED_BEARER_TOKEN]",
    ),
    (
        "aws_secret_key",
        re.compile(r"(?i)\bAWS_SECRET_ACCESS_KEY\s*[:=]\s*[\"']?[A-Za-z0-9/+=]{40}[\"']?"),
        "[REDACTED_AWS_SECRET_KEY]",
    ),
    (
        "slack_token",
        re.compile(r"\bxox[baprs]-[0-9]{10,13}-[0-9]{10,13}[a-zA-Z0-9-]*\b"),
        "[REDACTED_SLACK_TOKEN]",
    ),
    (
        "google_api_key",
        re.compile(r"\bAIza[0-9A-Za-z\\-_]{35}\b"),
        "[REDACTED_GOOGLE_API_KEY]",
    ),
    (
        "stripe_key",
        re.compile(r"\b(?:sk|rk)_(?:test|live)_[0-9a-zA-Z]{24}\b"),
        "[REDACTED_STRIPE_KEY]",
    ),
    (
        "jwt_token",
        re.compile(r"\beyJ[a-zA-Z0-9_-]+\.eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\b"),
        "[REDACTED_JWT]",
    ),
    (
        "secret_assignment",
        re.compile(
            r"(?i)(\b(?:api[_-]?key|access[_-]?key|secret|client[_-]?secret|password|passwd|token|auth[_-]?token)\b\s*[:=]\s*)([\"']?)[^\s,;\"'}]+(\2)"
        ),
        r"\1\2[REDACTED_SECRET]\3",
    ),
    (
        "json_yaml_secret",
        re.compile(
            r"(?i)([\"']?\b(?:apiKey|accessKey|clientSecret|secret|password|token)\b[\"']?\s*:\s*)([\"']?)[^\s,;\"'}]+(\2)"
        ),
        r"\1\2[REDACTED_SECRET]\3",
    ),
    (
        "connection_string",
        re.compile(r"(?i)\b(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis)://[^\s\"']+"),
        "[REDACTED_CONNECTION_STRING]",
    ),
)


def redact_secrets(text: str) -> RedactionResult:
    labels: list[str] = []
    count = 0
    redacted = text
    for label, pattern, replacement in _PATTERNS:
        redacted, substitutions = pattern.subn(replacement, redacted)
        if substitutions:
            count += substitutions
            labels.extend([label] * substitutions)
    return RedactionResult(redacted, count, tuple(labels))
