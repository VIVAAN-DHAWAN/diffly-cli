# diffly-cli

**diffly-cli** is a deterministic, terminal-first triage tool for large GitHub pull requests. It fetches the pull request metadata, changed files, unified diff, commit metadata, status checks, and repository tree; parses supported source changes with Tree-sitter; identifies a conservative blast-radius map; applies fixed risk rules; and emits a one-page Markdown review with a `SHIP`, `QUARANTINE`, or `BLOCK` verdict.

This is **Phase 1** of the product. It intentionally does not call an LLM. The prose “literate diff” explainer—background first, plain-language intent, and narrative code snippets—is planned for Phase 2 and is explicitly not part of this release.

## Why it exists

Large AI-generated pull requests can be difficult to review because file-by-file diffs hide the affected symbols, adjacent tests, dependency changes, and high-risk surfaces. diffly-cli makes the deterministic part of that review visible before an LLM is introduced.

## Install

Requirements are Python 3.10 or newer and a GitHub token that can read public repositories. A token is optional for light public use, but authenticated requests provide much higher API limits.

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install .
```

The package installs the `diffly-cli` command and uses Tree-sitter language packs for supported languages. The repository includes a lock-free, standard-library GitHub API client; no GitHub CLI installation is required to run the tool.

Set a token if needed:

```bash
export GITHUB_TOKEN="github_pat_..."
```

## Usage

```bash
diffly-cli pr <owner/repo> <pr-number>
```

Examples:

```bash
diffly-cli pr pallets/urllib3 3456
diffly-cli pr pallets/urllib3 3456 --output triage.md
diffly-cli pr pallets/urllib3 3456 --json
```

The command prints clean terminal Markdown by default. `--json` is provided for CI integration and `--output` saves the Markdown report to a file.

## Deterministic policy

| Verdict | Rule |
| --- | --- |
| **BLOCK** | A required check failed, or the pull request touches authentication, credentials, secrets, or security-sensitive files. |
| **QUARANTINE** | The pull request changes database schema or migrations, adds or changes dependencies, lacks obvious test coverage for a production file, or has unavailable/pending checks. |
| **SHIP** | No deterministic rule fired and observed checks passed. |

The policy is deliberately conservative. A verdict is a review gate, not a claim that a pull request is correct or safe in every context.

## What the blast-radius map contains

For each changed file, the report lists the file status, additions and deletions, changed symbols detected from supported source languages, direct call sites visible in changed hunks, and related test files discovered from the repository tree. The Phase 1 map is intentionally conservative: a full repository-wide call graph and cross-file symbol resolution are future work.

## Demo

The committed demo section is generated from real public GitHub pull requests and records the raw diff statistics beside diffly-cli’s one-page deterministic summary. It is updated as part of the Phase 1 validation run.

### Demo A: microsoft/vscode#330848

Raw GitHub PR statistics: **25 files**, **+2,557 / -251 lines**, **25 commits**. The one-page deterministic summary produced by diffly-cli is:

```text
Title: sessions: Add grid layout for chats
Checks: SUCCESS (27 observed)
Verdict: QUARANTINE
Reason: at least one changed production file lacks obvious test coverage
Risk flags: NO_TEST_COVERAGE
Blast radius: 25 changed files; changed symbols and direct callers listed per file
```

Full generated report: [`demo/vscode-330848.md`](demo/vscode-330848.md).

### Demo B: kubernetes/kubernetes#141413

Raw GitHub PR statistics: **41 files**, **+708 / -740 lines**, **1 commit**. The tool returned `QUARANTINE` because at least one changed production file lacked obvious test coverage; observed checks were successful.

Full generated report: [`demo/kubernetes-141413.md`](demo/kubernetes-141413.md).

### Demo C: astral-sh/ruff#27808

Raw GitHub PR statistics: **49 files**, **+1,675 / -254 lines**, **1 commit**. The tool returned `BLOCK` because observed checks failed, including CodSpeed and benchmark jobs.

Full generated report: [`demo/ruff-27808.md`](demo/ruff-27808.md).

## Current limitations

The **LLM-powered literate-diff explainer is not yet built**. There is no natural-language background/intent narrative, no model-generated code-snippet ordering, and no semantic explanation beyond deterministic metadata, symbol extraction, risk flags, and policy reasoning. Tree-sitter parsing currently focuses on symbols and direct calls visible in changed hunks, not a complete repository-wide reachability graph. Test coverage detection is heuristic and based on filenames and repository-tree evidence. GitHub checks are summarized from check runs and commit statuses; unavailable checks are quarantined rather than inferred to be passing.

## Roadmap

Phase 2 will add a provider-neutral literate-diff layer that consumes the deterministic JSON report plus selected diff context. It should support an explicit BYOK API configuration, bounded context windows, redaction of secrets before model calls, structured output validation, and a visible distinction between deterministic facts and generated prose.

## License

Released under the [MIT License](LICENSE).
