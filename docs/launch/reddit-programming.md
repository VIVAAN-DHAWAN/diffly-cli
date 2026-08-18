# Reddit r/programming draft

**Title:** I benchmarked a deterministic review gate against 18 large, agent-attributed GitHub PRs

I built [diffly-cli](https://github.com/VIVAAN-DHAWAN/diffly-cli), a small Python CLI that fetches a GitHub pull request, summarizes checks and changed files, builds a conservative blast-radius map, and emits one of three deterministic outcomes: `SHIP`, `QUARANTINE`, or `BLOCK`.

The aggregate benchmark is the main result. I selected **18 real public pull requests** with visible Claude, Codex, Copilot, Cursor, Aider, Devin, or AI-generated attribution and unusually large diffs. Diffly flagged **18/18** for a review gate: **5 BLOCK and 13 QUARANTINE**, covering **37,584 changed lines**. Under a stated proxy—300 changed lines/hour plus one minute/file for reading raw diffs, compared with two minutes plus ten seconds/file for the compact output—the modeled reading-time reduction is about **99%**.

This is not a claim about the correctness of those upstream projects, and the sample is not representative of GitHub. It is intentionally discovery-biased toward agent-attributed changes. I also kept the cases that look over-conservative: docs or generated assets with no natural unit tests, package metadata that triggered a dependency heuristic, and PRs with tests or passing checks where the coverage signal may be too broad. The output is a **review gate, not a safety certification**.

The three supporting live captures are:

- **VS Code #330848:** 25 files, +2,557/-251 lines, 25 commits, `QUARANTINE`, with 27 successful observed checks and a missing-obvious-test-coverage flag.
- **Kubernetes #141413:** 41 files, +708/-740 lines, 1 commit, `QUARANTINE`, with 2 observed checks and `tide` pending.
- **Ruff #27808:** 53 files, +1,845/-274 lines, 4 commits, `BLOCK`, with `CodSpeed Performance Analysis` failed.

The new GitHub Action adds the workflow integration:

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

An optional OpenAI-compatible BYOK explainer can add a bounded, redacted narrative, but it is clearly separated from the deterministic facts and cannot alter the verdict. I am interested in feedback on how teams would tune the false-positive boundary, especially for generated assets, documentation, dependency updates, and unavailable CI checks.
