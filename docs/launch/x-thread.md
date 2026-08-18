# X/Twitter thread draft

**1/10**
I built diffly-cli to make large GitHub pull requests easier to review before merge. The headline result is a benchmark across **18 real public agent-attributed PRs**: **18/18 were flagged**, with **5 BLOCK** and **13 QUARANTINE**, across **37,584 changed lines**.

**2/10**
That is not a claim that the projects or authors did something wrong. It is a conservative review-gate signal. The policy says: failed checks or security-sensitive paths can BLOCK; dependencies, database changes, missing obvious test coverage, or unavailable checks can QUARANTINE.

**3/10**
Using a transparent planning proxy—not observed reviewer timing—the raw-diff estimate is about 132.4 hours across the sample, versus about 1.8 hours for the compact Diffly summaries: roughly **99% modeled reading-time reduction**.

**4/10**
The sample is deliberately discovery-biased toward PRs whose titles or searchable bodies mention Claude, Codex, Copilot, Cursor, Aider, Devin, or AI-generated work. It is evidence about agent-sized changes, not a prevalence estimate for all GitHub PRs.

**5/10**
The table keeps the awkward cases. Some docs-heavy, asset-heavy, package-metadata, or test-adjacent PRs look over-conservative under filename-based heuristics. An accurate benchmark is more useful than a flattering one.

**6/10**
Supporting example: microsoft/vscode#330848 is 25 files and +2,557/-251 lines. Diffly returns QUARANTINE for missing obvious test coverage even though 27 observed checks are successful.

**7/10**
Supporting example: kubernetes/kubernetes#141413 is 41 files and +708/-740 lines. Its check state is pending with `tide`, so Diffly quarantines it instead of inferring that unavailable checks passed.

**8/10**
Supporting example: astral-sh/ruff#27808 is now 53 files, +1,845/-274 lines, and 4 commits. Diffly returns BLOCK because `CodSpeed Performance Analysis` failed.

**9/10**
The new GitHub Action posts or updates one PR comment with the verdict, risk flags, and collapsible blast-radius summary:

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

**10/10**
The optional BYOK explainer is separate from deterministic triage and cannot change the verdict. Diffly is a **review gate, not a safety certification**. Feedback on false positives and policy boundaries is welcome: https://github.com/VIVAAN-DHAWAN/diffly-cli
