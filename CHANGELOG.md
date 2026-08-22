# Changelog

All notable changes to diffly are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-08-22

Diffly 1.0.0 is the first production-ready release of the deterministic pull-request triage workflow. It stabilizes the command-line experience, interactive review, local analysis, GitHub Action, and explanation behavior around a clear three-outcome policy: healthy pull requests pass, focused review gates quarantine, and severe failures block.

### Added

- Reliable opted-in explanations: Diffly uses the configured AI provider when available and otherwise renders a clearly labelled local explanation from deterministic review facts.
- Automatic reuse of an authenticated `gh` session when `GITHUB_TOKEN` is not set.
- A centred terminal experience across the guided wizard, loading transition, interactive review, diagnostics, and focused report.
- Local analysis, stable JSON output, interactive review, GitHub Action integration, an update workflow, diagnostics, and guided setup as supported 1.0.0 workflows.

### Changed

- Rebalanced verdicts so `PASS` is the normal healthy outcome. Missing obvious test coverage, unavailable checks, and incomplete repository-tree hints remain visible as review notes instead of automatically forcing `QUARANTINE`.
- `QUARANTINE` is reserved for concrete review gates: security-sensitive code, database schema or migrations, dependency changes, and pending required checks.
- `BLOCK` is reserved for failed required checks and high-confidence credential exposure in a changed hunk.
- The guided prompts and recovery messages now give clearer next steps.
- Updated Diffly’s visual identity with the refreshed logo and terminal loading mark.

### Fixed

- Interactive mode no longer breaks imports on platforms without POSIX terminal support; it now falls back to the standard report.
- Running bare `diffly` in non-interactive environments (CI, pipes) prints help instead of hanging on prompts.
- Pressing Escape alone in the interactive selector no longer blocks waiting for arrow-key bytes.
- `CHECKS_PENDING` risk-flag evidence now lists the actual pending check names instead of the literal state string.
- Diff parsing ignores `\ No newline at end of file` markers when computing changed line numbers, fixing off-by-one symbol attribution.
- GitHub Action comment publishing distinguishes listing 404s (no comments yet) from publish failures via a typed error instead of string matching.

### Added

- **Local mode (`diffly local`):** triage git changes in any folder on disk — uncommitted working-tree edits by default, or a branch comparison with `--base main`. Works fully offline for private, archived, or removed repositories; untracked files are included and CI-check rules are skipped as not applicable.
- Generated explanations now render in the interactive review screen as a toggleable section, including clear setup guidance when no LLM key is configured.
- Loading spinners with progress messaging while pull-request data is fetched.
- Centered terminal composition across the wizard, setup walkthrough, interactive review, doctor, and version screens.
- The guided wizard prompts for a **Repository URL** with explicit format hints, confirms when deterministic-only mode was chosen, and accepts pasted pull-request URLs without asking for the number again.
- `-V` / `--version` flag on the root command and a `python -m diffly_cli` entry point.
- Guided wizard arguments are built from the real parser defaults so new options cannot drift between the wizard and the CLI.
- The repository argument now accepts full pull-request URLs (`diffly pr https://github.com/owner/repo/pull/12`), inferring the number; the guided wizard skips the number prompt when a URL is pasted.
- `CONTRIBUTING.md`, `SECURITY.md`, and this changelog.

### Changed

- Expanded LICENSE from the bare MIT template to a documented four-part license that keeps the standard MIT grant and adds definitions, contribution terms, verdict disclaimers, an extended warranty/liability statement, and general terms.
- Usage examples in the README and `--help` epilog point at live public pull requests.

## [0.2.1] - 2026-08-21

### Changed

- Renamed the all-clear verdict from `SHIP` to `PASS`; `SHIP` remains accepted as a legacy alias and `legacy_verdict` preserves it in JSON output.
- `diffly` is now the primary executable name with `diffly-cli` kept as a compatibility alias.
- Consolidated the interactive UX: bare `diffly` opens the guided PR wizard, plus new `setup`, `doctor`, `help`, and `version` subcommands.
- Pending checks are quarantined explicitly (`CHECKS_PENDING`) rather than folded into unknown-check handling.

## [0.2.0] - 2026-08-20

### Added

- Hardened triage for large and incomplete GitHub responses: paginated files, commits, check runs, statuses, and repository tree; raw-diff fallback when the unified diff exceeds GitHub's size limit.

## [0.1.0] - 2026-08-18

### Added

- Phase 1 deterministic triage: blast-radius map, fixed risk rules, one-page Markdown report, stable JSON output, and the bundled GitHub Action.
- Phase 2 optional literate-diff explainer with strict output validation, secret redaction, and fail-closed behavior.
