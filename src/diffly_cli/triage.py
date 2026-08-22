from __future__ import annotations

import fnmatch
import re
from collections import defaultdict
from typing import Any

from .models import ChangedFile, PRMetadata, RiskFlag
from .redact import redact_secrets

AUTH_PATTERNS = ["*auth*", "*login*", "*oauth*", "*credential*", "*secret*", "*.pem", "*.key", ".env", ".env.*", "*password*", "*security*", "*iam*"]
DB_PATTERNS = ["*migration*", "*migrations*", "*schema*", "*alembic*", "*prisma*", "*.sql"]
TEST_PATTERNS = ["test*", "tests*", "spec*", "*_test.*", "*.test.*", "*.spec.*"]
DEPENDENCY_FILES = {
    "package.json", "package-lock.json", "npm-shrinkwrap.json", "yarn.lock", "pnpm-lock.yaml",
    "pyproject.toml", "poetry.lock", "requirements.txt", "requirements-dev.txt", "Pipfile", "Pipfile.lock",
    "go.mod", "go.sum", "Cargo.toml", "Cargo.lock", "Gemfile", "Gemfile.lock", "pom.xml", "build.gradle",
}


def _matches(path: str, patterns: list[str]) -> bool:
    lowered = path.lower()
    return any(fnmatch.fnmatch(lowered, pattern.lower()) or fnmatch.fnmatch(lowered.split("/")[-1], pattern.lower()) for pattern in patterns)


def _is_production_file(path: str) -> bool:
    lowered = path.lower()
    parts = lowered.split("/")
    if any(part in {"docs", "examples", "fixtures", "generated", "tests", "test"} for part in parts):
        return False
    if _matches(path, TEST_PATTERNS):
        return False
    return not lowered.endswith((".md", ".txt", ".json")) and lowered != "install.sh"


def _added_dependency_names(file: ChangedFile) -> list[str]:
    if file.path.rsplit("/", 1)[-1] not in DEPENDENCY_FILES:
        return []
    values: list[str] = []
    for line in file.patch.splitlines():
        if line.startswith("+") and not line.startswith("+++"):
            match = re.search(r"[\"']([@A-Za-z0-9_./-]+)[\"']\s*[:=]", line)
            if match:
                values.append(match.group(1))
            elif re.search(r"^[+]\s*[A-Za-z0-9_.-]+[=<>~]", line):
                values.append(line[1:].strip().split()[0])
    return sorted(dict.fromkeys(values))


def _test_files(files: list[ChangedFile]) -> list[str]:
    return [file.path for file in files if _matches(file.path, TEST_PATTERNS)]


def _covered_by_test(file: ChangedFile, test_paths: list[str]) -> list[str]:
    stem = file.path.rsplit("/", 1)[-1].rsplit(".", 1)[0].lower()
    matches = []
    for test_path in test_paths:
        name = test_path.rsplit("/", 1)[-1].lower()
        if stem in name or file.path.rsplit("/", 1)[0].lower() in test_path.lower():
            matches.append(test_path)
    return matches


def _has_exposed_secret(file: ChangedFile) -> bool:
    """Detect a credential-like value added in the changed hunk, not just its path."""
    added_lines = "\n".join(line[1:] for line in file.patch.splitlines() if line.startswith("+") and not line.startswith("+++"))
    # A generic ``token = os.getenv(...)`` assignment is common application
    # code, not evidence of an exposed credential. Block only on high-confidence
    # credential formats (keys, bearer tokens, private keys, connection URLs).
    redacted = redact_secrets(added_lines)
    return any(label != "secret_assignment" for label in redacted.labels)


def compute_flags(metadata: PRMetadata, files: list[ChangedFile], checks: dict[str, Any], repo_paths: list[str] | None = None) -> list[RiskFlag]:
    flags: list[RiskFlag] = []
    tree_complete = bool(checks.get("repository_tree_complete", repo_paths is not None))
    test_paths = [path for path in (repo_paths or []) if _matches(path, TEST_PATTERNS)] if tree_complete else []
    changed_test_paths = _test_files(files)
    if not tree_complete:
        flags.append(RiskFlag("REPOSITORY_TREE_INCOMPLETE", "low", "Repository file listing was unavailable or truncated; test-coverage hints may be incomplete.", ["repository tree incomplete"]))

    exposed_secrets = [file.path for file in files if _has_exposed_secret(file)]
    if exposed_secrets:
        flags.append(RiskFlag("EXPOSED_SECRET", "critical", "Adds a credential-like value in the changed code or configuration.", exposed_secrets))

    auth_files = [file.path for file in files if not _matches(file.path, TEST_PATTERNS) and _matches(file.path, AUTH_PATTERNS)]
    if auth_files:
        flags.append(RiskFlag("AUTH_OR_SECRET", "high", "Touches authentication, credentials, secrets, or security-sensitive code that deserves focused review.", auth_files))

    db_files = [file.path for file in files if _matches(file.path, DB_PATTERNS)]
    if db_files:
        flags.append(RiskFlag("DATABASE_CHANGE", "high", "Touches database schema, models, migrations, or SQL.", db_files))

    dependency_evidence: list[str] = []
    for file in files:
        names = _added_dependency_names(file)
        if names:
            dependency_evidence.append(f"{file.path}: {', '.join(names)}")
        elif file.path.rsplit("/", 1)[-1] in DEPENDENCY_FILES and file.additions > 0:
            dependency_evidence.append(file.path)
    if dependency_evidence:
        flags.append(RiskFlag("NEW_DEPENDENCY", "medium", "Adds or changes a dependency manifest or lockfile.", dependency_evidence))

    untested: list[str] = []
    for file in files:
        if _matches(file.path, TEST_PATTERNS):
            continue
        coverage = _covered_by_test(file, test_paths + changed_test_paths)
        file.tests_found = coverage
        if _is_production_file(file.path) and not coverage:
            untested.append(file.path)
    if untested and tree_complete:
        flags.append(RiskFlag("NO_TEST_COVERAGE", "low", "Changed production files have no obvious neighboring or repository test coverage; this is a review hint, not a verdict gate.", untested[:50]))

    check_state = str(checks.get("state", "unknown"))
    if check_state == "not_applicable":
        # Local mode has no CI; skip check-derived flags entirely.
        return flags
    if check_state == "failure":
        flags.append(RiskFlag("CHECKS_FAILED", "critical", "One or more required status checks failed.", list(checks.get("failed", []))))
    elif check_state == "pending":
        flags.append(RiskFlag("CHECKS_PENDING", "medium", "Required status checks are still pending.", list(checks.get("pending", [])) or [check_state]))
    elif check_state != "success":
        flags.append(RiskFlag("CHECKS_UNKNOWN", "low", "Status checks are missing or unavailable; this is informational, not a failure.", [check_state]))

    return flags


def verdict_for(flags: list[RiskFlag], checks: dict[str, Any]) -> tuple[str, list[str]]:
    codes = {flag.code for flag in flags}
    reasoning: list[str] = []
    if "CHECKS_FAILED" in codes:
        reasoning.append("BLOCK because at least one status check failed.")
        return "BLOCK", reasoning
    if "EXPOSED_SECRET" in codes:
        reasoning.append("BLOCK because the pull request appears to add a credential-like value.")
        return "BLOCK", reasoning
    if "AUTH_OR_SECRET" in codes:
        reasoning.append("QUARANTINE because authentication or security-sensitive code changed and needs focused review.")
    if "DATABASE_CHANGE" in codes:
        reasoning.append("QUARANTINE because database schema or migration changes require an explicit review gate.")
    if "NEW_DEPENDENCY" in codes:
        reasoning.append("QUARANTINE because dependency changes expand the supply-chain and runtime surface.")
    if "CHECKS_PENDING" in codes:
        reasoning.append("QUARANTINE because required checks are still running.")
    if reasoning:
        return "QUARANTINE", reasoning
    observations: list[str] = []
    if "NO_TEST_COVERAGE" in codes:
        observations.append("no obvious test coverage was found for one or more production files")
    if "CHECKS_UNKNOWN" in codes:
        observations.append("status checks were unavailable")
    if "REPOSITORY_TREE_INCOMPLETE" in codes:
        observations.append("repository-wide test hints were incomplete")
    if observations:
        local_note = " local analysis has no CI checks." if str(checks.get("state")) == "not_applicable" else ""
        reasoning.append(f"PASS with review notes: {'; '.join(observations)}.{local_note}")
        return "PASS", reasoning
    if str(checks.get("state")) == "not_applicable":
        reasoning.append("PASS because no blocking or quarantine rule fired (local analysis has no CI checks).")
    else:
        reasoning.append("PASS because no blocking or quarantine rule fired and all observed checks passed.")
    return "PASS", reasoning
