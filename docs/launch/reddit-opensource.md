# Reddit r/opensource draft

**Title:** diffly-cli: an open-source GitHub PR triage tool with a deterministic review gate and Action wrapper

I am releasing [diffly-cli](https://github.com/VIVAAN-DHAWAN/diffly-cli), an open-source, terminal-first tool for making large GitHub pull requests easier to inspect. It fetches metadata, changed files, diffs, commits, checks, and repository-tree evidence; identifies a conservative blast radius; and emits `SHIP`, `QUARANTINE`, or `BLOCK` before an optional LLM explainer is considered.

The primary evidence is a benchmark of **18 real public pull requests** with visible Claude, Codex, Copilot, Cursor, Aider, Devin, or AI-generated attribution and large changes. Diffly flagged **18/18** for a review gate: **5 BLOCK and 13 QUARANTINE**, across **37,584 changed lines**. A transparent proxy estimates about **99% less reading time** for the compact summaries than for raw diffs: 300 changed lines/hour plus one minute/file for raw review versus two minutes plus ten seconds/file for the Diffly output. These are modeled estimates, not a user study.

The sample is discovery-biased and is not meant to say that all agent-generated PRs have this profile. The benchmark also includes likely false positives and conservative calls. That is important because the tool is a **review gate, not a safety certification**: it surfaces reasons to pause, not proof that a change is unsafe or incorrect.

The live supporting captures cover three different projects:

- VS Code #330848: 25 files, +2,557/-251 lines, 25 commits, `QUARANTINE` for missing obvious test coverage despite 27 successful observed checks.
- Kubernetes #141413: 41 files, +708/-740 lines, 1 commit, `QUARANTINE` because `tide` remains pending and test coverage is not obvious.
- Ruff #27808: 53 files, +1,845/-274 lines, 4 commits, `BLOCK` because `CodSpeed Performance Analysis` failed.

The merged GitHub Action keeps setup small and updates one PR comment rather than duplicating comments:

```yaml
name: Diffly
on: pull_request
permissions:
  contents: read
  pull-requests: write
jobs:
  diffly:
    runs-on: ubuntu-latest
    steps:
      - uses: VIVAAN-DHAWAN/diffly-cli@main
```

The deterministic path works without an LLM or LLM key. If configured, the optional explainer receives bounded, redacted context and cannot change the deterministic verdict. The project is intentionally conservative and would benefit from feedback on organization-specific policies, coverage heuristics, and where a gate should become an informational warning.
