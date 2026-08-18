# Show HN draft

**Title:** Show HN: diffly-cli – deterministic review gates for large agent-attributed PRs

Large pull requests produced with coding agents are not necessarily wrong, but they can be expensive to understand before merge. I built [diffly-cli](https://github.com/VIVAAN-DHAWAN/diffly-cli) to make the first review pass deterministic: fetch a GitHub PR, summarize its checks and changed files, map visible symbols and direct callers, identify dependency/database/auth/test-coverage risk signals, and emit `SHIP`, `QUARANTINE`, or `BLOCK`.

The headline result is the benchmark, not a single hand-picked example. I ran Diffly against **18 real public pull requests with visible Claude, Codex, Copilot, Cursor, Aider, Devin, or AI-generated attribution and large diffs**. It flagged **18/18** for a review gate: **5 BLOCK and 13 QUARANTINE**, across **37,584 changed lines**. Using a transparent proxy rather than observed reviewer timings—300 changed lines/hour plus one minute per file for the raw diff, versus two minutes plus ten seconds per file for the compact summary—the modeled reading-time reduction is approximately **99%**.

The benchmark is intentionally discovery-biased toward PRs whose titles or searchable bodies identify an AI coding tool, so it is not a prevalence estimate for GitHub as a whole. The table includes cases where the rules look conservative: documentation- or asset-heavy changes, package metadata, and coverage heuristics that fired even when tests or checks suggested the gate might be stronger than necessary. The policy is a **review gate, not a safety certification**.

Three live public PR captures are included as supporting detail. VS Code #330848 is a 25-file, +2,557/-251-line change that received `QUARANTINE` for missing obvious test coverage while checks were successful. Kubernetes #141413 is a 41-file, +708/-740-line change with a pending `tide` check, so Diffly quarantines it rather than inferring that unavailable checks passed. Ruff #27808 is now a 53-file, +1,845/-274-line, 4-commit change that receives `BLOCK` because `CodSpeed Performance Analysis` failed.

There is also a GitHub Action, so the result can be posted directly to a PR without a separate checkout step:

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

The optional explainer accepts the same BYOK LLM environment variables as the CLI, but deterministic facts and the verdict remain authoritative. With no key, the Action runs deterministic-only.

I would especially appreciate feedback on the false-positive boundary: when should a dependency, documentation, generated asset, or missing-check signal be a hard review gate, and when should it be informational? The goal is not to replace reviewers or certify safety; it is to make the first pass more legible and consistent.
