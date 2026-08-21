# diffly-cli Security and Reliability Audit

## Scope and method

This audit exercised `diffly-cli` against one current public pull request from each of 20 distinct repositories, in addition to the repository’s unit tests and targeted regression tests. The test matrix used authenticated GitHub REST requests, structured JSON output, and live changed-file, check, status, and repository-tree responses. The audit was passive: it analyzed public pull-request data and did not modify any external repository.

The baseline suite contained 15 passing tests. The first live matrix produced 19 successful JSON runs and one failure: `tensorflow/tensorflow#125680` exited with code 2 because GitHub rejected its raw diff as too large. Additional targeted testing exposed two latent regressions in the analyzer and JSON output path.

## Findings and remediation

| ID | Severity | Finding | Effect | Remediation |
| --- | --- | --- | --- | --- |
| F-01 | High reliability | Raw pull-request diff was fetched unconditionally. GitHub can return HTTP 406 with `too_large` for a diff exceeding its generated-diff limit. | Large pull requests aborted before deterministic triage, even when the paginated files endpoint had returned useful metadata and patches. | Raw diff retrieval is now best-effort. File metadata and available patches remain usable when the raw diff is unavailable. |
| F-02 | High correctness | API-provided patches were never parsed into hunks before changed-line mapping. | Touched symbols and direct callers were systematically empty for normal GitHub API responses. | `analyze_file()` now parses the patch into hunks before computing changed line numbers. |
| F-03 | High reliability | Once hunks were populated, `--json` serialized nested `Hunk` dataclasses through `file.__dict__`. | Structured output crashed with `TypeError: Object of type Hunk is not JSON serializable`. | JSON output now uses recursive dataclass serialization with `dataclasses.asdict()`. |
| F-04 | Medium correctness | The combined commit-status `error` state was mapped to pending. GitHub defines the combined state as failure when any context reports `error` or `failure`. | A failing status could be downgraded to `QUARANTINE` instead of `BLOCK`. | Combined and individual `error` statuses are now treated as failures. |
| F-05 | Medium correctness | Recursive repository-tree responses discarded the `truncated` field. | Missing files in large repositories could produce a false definitive `NO_TEST_COVERAGE` result. | Tree completeness is preserved; unavailable or truncated trees produce `REPOSITORY_TREE_INCOMPLETE` and suppress definitive repository-wide coverage conclusions. |
| F-06 | Medium reliability | Check-run and commit-status retrieval requested only the first 100 results. | Repositories with more than 100 checks or statuses could be incorrectly summarized as passing or incomplete. | Both endpoints now paginate until all reported results are collected. |
| F-07 | Medium input safety | Repository parsing accepted query, fragment, percent-encoded path, and other non-name characters. | Malformed input could alter the API path or produce confusing downstream failures. | Owner and repository components now accept only GitHub-compatible name characters. |
| F-08 | Low tooling reliability | `scripts/validate_action.py` imported PyYAML, but the declared development extra did not install it. | A repository-provided validation command failed in a clean development environment before testing any YAML invariants. | `PyYAML>=6` is now declared in the `dev` extra. |

The large-diff behavior is consistent with GitHub’s documented separation between raw pull-request diff media types and the paginated list-files endpoint [1]. GitHub’s own tree documentation states that `truncated: true` means the recursive result exceeded its maximum and recommends retrieving subtrees non-recursively [2]. GitHub’s combined-status documentation explicitly defines `error` and `failure` as failure conditions [3]. A real-world automation issue reports the same 406 `too_large` failure and recommends the list-files API as a fallback [4].

## Cross-repository validation

After the fixes, all 20 matrix entries completed with exit code 0 and valid JSON. The formerly failing TensorFlow pull request returned 260 changed-file records despite the rejected raw diff. Symbol detection was populated for source-bearing files across the matrix, and the Rust case correctly surfaced an incomplete repository tree rather than asserting definitive repository-wide coverage.

| Repository | PR | Exit | Verdict | Files | Files with symbols | Notable flags |
| --- | ---: | ---: | --- | ---: | ---: | --- |
| `microsoft/vscode` | 331665 | 0 | QUARANTINE | 11 | 11 | `NO_TEST_COVERAGE`, `CHECKS_UNKNOWN` |
| `kubernetes/kubernetes` | 141468 | 0 | QUARANTINE | 4 | 4 | `CHECKS_UNKNOWN` |
| `astral-sh/ruff` | 27894 | 0 | QUARANTINE | 1 | 1 | `CHECKS_UNKNOWN` |
| `python/cpython` | 156059 | 0 | BLOCK | 3 | 3 | `CHECKS_FAILED` |
| `pytorch/pytorch` | 194090 | 0 | QUARANTINE | 1 | 1 | `CHECKS_UNKNOWN` |
| `tensorflow/tensorflow` | 125680 | 0 | QUARANTINE | 260 | 254 | `NO_TEST_COVERAGE`, `CHECKS_UNKNOWN` |
| `rust-lang/rust` | 161362 | 0 | QUARANTINE | 6 | 6 | `REPOSITORY_TREE_INCOMPLETE`, `CHECKS_UNKNOWN` |
| `golang/go` | 80948 | 0 | QUARANTINE | 3 | 3 | `CHECKS_UNKNOWN` |
| `facebook/react` | 37325 | 0 | QUARANTINE | 2 | 2 | `NO_TEST_COVERAGE`, `CHECKS_UNKNOWN` |
| `nodejs/node` | 65404 | 0 | QUARANTINE | 1 | 1 | `CHECKS_UNKNOWN` |
| `numpy/numpy` | 32346 | 0 | QUARANTINE | 20 | 20 | `NO_TEST_COVERAGE`, `CHECKS_UNKNOWN` |
| `pandas-dev/pandas` | 66851 | 0 | QUARANTINE | 9 | 9 | `NO_TEST_COVERAGE`, `CHECKS_UNKNOWN` |
| `django/django` | 21802 | 0 | BLOCK | 1 | 1 | `CHECKS_FAILED` |
| `rails/rails` | 58518 | 0 | QUARANTINE | 4 | 4 | `NO_TEST_COVERAGE` |
| `github/docs` | 45547 | 0 | QUARANTINE | 1 | 1 | `NO_TEST_COVERAGE`, `CHECKS_UNKNOWN` |
| `home-assistant/core` | 179583 | 0 | BLOCK | 11 | 11 | `NO_TEST_COVERAGE`, `CHECKS_FAILED` |
| `ansible/ansible` | 87426 | 0 | BLOCK | 2 | 2 | `CHECKS_FAILED` |
| `docker/compose` | 14096 | 0 | BLOCK | 2 | 2 | `CHECKS_FAILED` |
| `curl/curl` | 22624 | 0 | SHIP | 1 | 1 | None |
| `apache/airflow` | 71849 | 0 | QUARANTINE | 1 | 0 | `CHECKS_UNKNOWN` |

## Regression coverage

The added regression suite covers large raw-diff failure recovery, raw-diff patch enrichment, hunk-to-symbol mapping, nested JSON serialization, truncated repository trees, combined-status errors, check-run pagination, commit-status pagination, and malformed repository arguments. The action formatter and YAML invariant validator were also executed successfully after declaring the missing PyYAML development dependency. The final local validation completed with **21 passing tests**, successful bytecode compilation, no whitespace errors, and no broken virtual-environment requirements.

## References

[1]: https://docs.github.com/en/rest/pulls/pulls?apiVersion=2026-03-10#list-pull-requests-files "GitHub REST API: List pull requests files"

[2]: https://docs.github.com/en/rest/git/trees?apiVersion=2026-03-10 "GitHub REST API: Git trees"

[3]: https://docs.github.com/en/rest/commits/statuses?apiVersion=2026-03-10 "GitHub REST API: Commit statuses"

[4]: https://github.com/reviewdog/reviewdog/issues/1696 "reviewdog issue: GitHub Pull Request diff API responds with 406 — diff too large"
