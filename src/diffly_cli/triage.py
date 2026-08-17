from __future__ import annotations

import fnmatch
import re
from collections import defaultdict
from typing import Any

from .models import ChangedFile, PRMetadata, RiskFlag

AUTH_PATTERNS = [
    "*auth*", "*login*", "*oauth*", "*credential*", "*secret*", "*.pem", "*.key",
    ".env", ".env.*", "*token*", "*password*", "*security*", "*iam*",
]
DB_PATTERNS = ["*migration*", "*migrations*", "*schema*", "*alembic*", "*prisma*", "*.sql", "*db*model*"]
TEST_PATTERNS = ["test*", "tests*", "spec*", "*_test.*", "*.test.*", "*.spec.*"]
DEPENDENCY_FILES = {
    "package.json", "package-lock.json", "npm-shrinkwrap.json", "yarn.lock", "pnpm-lock.yaml",
    "pyproject.toml", "poetry.lock", "requirements.txt", "requirements-dev.txt", "Pipfile", "Pipfile.lock",
    "go.mod", "go.sum", "Cargo.toml", "Cargo.lock", "Gemfile", "Gemfile.lock", "pom.xml", "build.gradle",
}


def _matches(path: str, patterns: list[str]) -> bool:
    lowered = path.lower()
    return any(fnmatch.fnmatch(lowered, pattern.lower()) or fnmatch.fnmatch(lowered.split("/")[-1], pattern.lower()) for pattern in patterns)


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


def compute_flags(metadata: PRMetadata, files: list[ChangedFile], checks: dict[str, Any], repo_paths: list[str] | None = None) -> list[RiskFlag]:
    flags: list[RiskFlag] = []
    test_paths = [path for path in (repo_paths or []) if _matches(path, TEST_PATTERNS)]
    changed_test_paths = _test_files(files)

    auth_files = [file.path for file in files if _matches(file.path, AUTH_PATTERNS)]
    if auth_files:
        flags.append(RiskFlag("AUTH_OR_SECRET", "high", "Touches authentication, credentials, secrets, or security-sensitive files.", auth_files))

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
        if not coverage:
            untested.append(file.path)
    if untested:
        flags.append(RiskFlag("NO_TEST_COVERAGE", "medium", "Changed production files have no obvious neighboring or repository test coverage.", untested[:50]))

    check_state = str(checks.get("state", "unknown"))
    if check_state == "failure":
        flags.append(RiskFlag("CHECKS_FAILED", "critical", "One or more required status checks failed.", list(checks.get("failed", []))))
    elif check_state != "success":
        flags.append(RiskFlag("CHECKS_UNKNOWN", "medium", "Required status checks are missing, pending, or unavailable.", [check_state]))

    return flags


def verdict_for(flags: list[RiskFlag], checks: dict[str, Any]) -> tuple[str, list[str]]:
    codes = {flag.code for flag in flags}
    reasoning: list[str] = []
    if "CHECKS_FAILED" in codes:
        reasoning.append("BLOCK because at least one status check failed.")
        return "BLOCK", reasoning
    if "AUTH_OR_SECRET" in codes:
        reasoning.append("BLOCK because the pull request touches authentication, credentials, secrets, or security-sensitive files.")
        return "BLOCK", reasoning
    if "DATABASE_CHANGE" in codes:
        reasoning.append("QUARANTINE because database schema or migration changes require an explicit review gate.")
    if "NEW_DEPENDENCY" in codes:
        reasoning.append("QUARANTINE because dependency changes expand the supply-chain and runtime surface.")
    if "NO_TEST_COVERAGE" in codes:
        reasoning.append("QUARANTINE because at least one changed production file lacks obvious test coverage.")
    if "CHECKS_UNKNOWN" in codes:
        reasoning.append("QUARANTINE because the affected pull request does not have a confirmed passing check result.")
    if reasoning:
        return "QUARANTINE", reasoning
    reasoning.append("SHIP because no deterministic risk rule fired and all observed checks passed.")
    return "SHIP", reasoning
