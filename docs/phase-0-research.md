# Phase 0 research and assumptions

> Historical note: this document records the initial research and implementation assumptions. The Phase 2 explainer described below was subsequently implemented; see `docs/phase-2-contract.md` and the current README for the shipped behavior.

## Name selection

The requested candidate names were checked on GitHub, npm, and PyPI on 2026-08-17. `diffly` was rejected because it is already an active unrelated Polars DataFrame comparison package on both [GitHub](https://github.com/Quantco/diffly) and [PyPI](https://pypi.org/project/diffly/). `diffly-cli` was the first candidate in the requested order with no exact npm package and no exact PyPI project; GitHub search returned only unrelated repositories whose names merely contained the term. The repository is therefore named `diffly-cli`.

## Existing-tool check

Searches found adjacent projects, including [ruleblast](https://github.com/Kpoiut/ruleblast), which maps the blast radius of agent instruction-file changes, and other code-impact/dependency-graph tools. None of the reviewed projects combined all requested capabilities: accepting a GitHub pull request, producing a prose literate-diff explanation, computing a code reachability/blast-radius map, and emitting deterministic `SHIP` / `QUARANTINE` / `BLOCK` verdicts. No exact actively maintained duplicate was found.

## Language choice

Python was selected because the current Tree-sitter ecosystem provides a stable core binding plus a maintained language-pack distribution that exposes parsers for multiple languages through one dependency. The CLI is intentionally small and uses Python’s standard library for HTTP requests, which keeps authentication and installation behavior easy to inspect.

## Implementation assumptions

The tool treats a missing or pending check result as `QUARANTINE`; it never infers that unavailable checks passed. Authentication, credential, secret, and security-sensitive path changes are `BLOCK` by policy. Database/schema/migration changes, dependency changes, and changed production files without obvious test coverage are `QUARANTINE`. A `SHIP` verdict requires no rule to fire and observed checks to pass.

The Phase 1 blast-radius map is conservative. It reports changed files, symbols and direct calls found in changed hunks, plus test files inferred from repository-tree names. It does not claim to be a full repository-wide call graph. Test coverage is heuristic and may produce false positives or false negatives.

GitHub’s pull-request file-list endpoint returned HTTP 404 for the selected closed public demo PRs even though the pull-request metadata and raw diff were available. The client therefore falls back to parsing the raw unified diff when that endpoint returns 404. The fallback preserves file paths, status, additions, deletions, and hunks, while API-provided file metadata is preferred whenever available.

## Phase 2 boundary

At the time of this Phase 0 note, the LLM literate-diff explainer was not implemented. It was subsequently added as the optional Phase 2 feature described in `docs/phase-2-contract.md`: it consumes deterministic JSON plus bounded diff context, redacts secrets before model calls, validates structured output, and labels generated prose separately from facts returned by GitHub or the local analyzer.
