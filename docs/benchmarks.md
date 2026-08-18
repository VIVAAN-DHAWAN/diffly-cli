# Benchmark: agent-sized public pull requests

Across **18 recent public pull requests** selected for visible Claude, Codex, Copilot, Cursor, Aider, Devin, or AI-generated attribution and large diffs, Diffly retrospectively flagged **18/18** of these merged PRs as requiring a gate: 5 BLOCK and 13 QUARANTINE; 0 were SHIP. The sample contains **37,584 changed lines**; under the stated proxy, the raw-diff reading estimate is **132.4 h** versus **1.8 h** for the compact Diffly output, a modeled reduction of **99%**, not an observed timing study.

The selection is deliberately discovery-biased toward PRs whose title or searchable body names an AI coding tool, so it is evidence about agent-sized, agent-attributed changes—not a prevalence estimate for all GitHub pull requests. The table preserves cases where the deterministic rules look conservative or potentially wrong instead of treating every flag as a success.

**Reading-time proxy.** A changed line is treated as one unit of review effort at **300 changed lines/hour (5/minute)**, with **one additional minute per changed file** for navigation and context switching. Diffly is modeled as **two minutes plus 10 seconds per changed file** for reading its compact summary output. These are transparent planning assumptions, not measurements; the file-count term is included because code-review guidance consistently treats smaller, more focused PRs as easier to review [1].

| Public PR | Primary language | Size | Diffly verdict | Risk flags caught | Raw diff vs. Diffly | Honest read |
| --- | --- | ---: | --- | --- | ---: | --- |
| [Cagatay342/openusage#1][pr2] | Swift | 26 files / +1997/-53 | **BLOCK** | `AUTH_OR_SECRET`, `NO_TEST_COVERAGE`, `CHECKS_FAILED` | 7.3 h / 6.3 min | BLOCK is well-supported: auth-store changes and a failed build/test check. |
| [Gegcuk/QuizMaker#756][pr3] | Java | 9 files / +956/-25 | **QUARANTINE** | `NO_TEST_COVERAGE` | 3.4 h / 3.5 min | Likely conservative: the evidence includes new tests, but the heuristic still flags coverage on other changed production files. |
| [JinnZ2/CEED#2][pr4] | Python | 10 files / +3013/-1294 | **QUARANTINE** | `NO_TEST_COVERAGE`, `CHECKS_UNKNOWN` | 14.5 h / 3.7 min | Possibly conservative: a very large mixed code/docs/experiment change with no reported checks. |
| [Kirt22/Journal.IO-mono-repo#70][pr5] | TypeScript | 44 files / +4515/-264 | **BLOCK** | `AUTH_OR_SECRET`, `NEW_DEPENDENCY`, `NO_TEST_COVERAGE`, `CHECKS_UNKNOWN` | 16.7 h / 9.3 min | BLOCK is well-supported by auth-sensitive changes; unknown checks add a separate quarantine signal. |
| [attunehq/nudge#72][pr6] | Rust | 31 files / +1752/-69 | **QUARANTINE** | `NEW_DEPENDENCY`, `NO_TEST_COVERAGE` | 6.6 h / 7.2 min | Reasonable quarantine: dependency and broad hook/reference changes deserve review even though checks passed. |
| [augentic/omnia-backends#55][pr7] | Rust | 8 files / +883/-774 | **QUARANTINE** | `NEW_DEPENDENCY`, `NO_TEST_COVERAGE` | 5.7 h / 3.3 min | Possibly conservative: a Cursor integration with dependency changes and passing checks was quarantined for coverage. |
| [corosolto/client#205][pr8] | JavaScript | 24 files / +365/-518 | **QUARANTINE** | `NEW_DEPENDENCY`, `NO_TEST_COVERAGE` | 3.3 h / 6.0 min | Likely conservative: the PR is documentation/AI-attribution heavy, but package metadata and heuristic coverage rules fired. |
| [ferrreo/local-image-detect-chrome#7][pr9] | TypeScript | 44 files / +1906/-25 | **BLOCK** | `NO_TEST_COVERAGE`, `CHECKS_FAILED` | 7.2 h / 9.3 min | BLOCK is well-supported by a failed Chrome integration check; the asset-heavy diff also lacks obvious tests. |
| [flatpark/flatpark#211][pr10] | Shell | 12 files / +539/-0 | **QUARANTINE** | `NO_TEST_COVERAGE` | 2.0 h / 4.0 min | Likely conservative: packaging/registry assets are not naturally unit-tested, yet the coverage heuristic fired. |
| [fwaris/FsHarness#4][pr11] | F# | 24 files / +1030/-129 | **QUARANTINE** | `NO_TEST_COVERAGE`, `CHECKS_UNKNOWN` | 4.3 h / 6.0 min | Possibly conservative: editor cache artifacts and docs dominate the diff; checks were unavailable rather than failed. |
| [joangarvin/travseeker#22][pr12] | TypeScript | 30 files / +1024/-195 | **BLOCK** | `AUTH_OR_SECRET`, `NO_TEST_COVERAGE` | 4.6 h / 7.0 min | Potentially conservative on the auth flag because the evidence is stylesheet tokens; the final BLOCK also reflects the absence of obvious tests. |
| [laurilehtinen/ccusage#2][pr13] | Rust | 42 files / +3939/-201 | **QUARANTINE** | `DATABASE_CHANGE`, `NEW_DEPENDENCY`, `NO_TEST_COVERAGE`, `CHECKS_UNKNOWN` | 14.5 h / 9.0 min | Reasonable quarantine: dependency/schema changes and unavailable checks create a substantial review gate. |
| [powabase-ai/powabase-ai#46][pr14] | Python | 26 files / +4964/-286 | **BLOCK** | `AUTH_OR_SECRET`, `DATABASE_CHANGE`, `NO_TEST_COVERAGE` | 17.9 h / 6.3 min | BLOCK is plausible: auth-sensitive tests and database migrations are both present, despite passing observed checks. |
| [springbrand-lab/springbrand-agent-setup#13][pr15] | Python | 17 files / +901/-23 | **QUARANTINE** | `NO_TEST_COVERAGE` | 3.4 h / 4.8 min | Possibly conservative: this is largely agent/plugin documentation and workflow material with passing checks. |
| [vshulcz/deja-vu#396][pr16] | Go | 10 files / +536/-11 | **QUARANTINE** | `NO_TEST_COVERAGE` | 2.0 h / 3.7 min | Likely conservative: Aider history and docs dominate; the heuristic treats the lack of nearby tests as a quarantine signal. |
| [workcrewlabs/worker-pc-app#45][pr17] | TypeScript | 28 files / +767/-111 | **QUARANTINE** | `NEW_DEPENDENCY`, `NO_TEST_COVERAGE`, `CHECKS_UNKNOWN` | 3.4 h / 6.7 min | Reasonable quarantine: broad desktop changes, dependency metadata, and unavailable checks. |
| [xiaoqiuuuu/Codex-Pulse#3][pr18] | Rust | 16 files / +2018/-248 | **QUARANTINE** | `NEW_DEPENDENCY`, `NO_TEST_COVERAGE` | 7.8 h / 4.7 min | Reasonable quarantine: test-script dependency changes and broad Rust/Tauri changes merit review. |
| [ycoj/YCOJ#18][pr19] | TypeScript | 29 files / +2243/-10 | **QUARANTINE** | `NEW_DEPENDENCY`, `NO_TEST_COVERAGE` | 8.0 h / 6.8 min | Reasonable quarantine: AI-generation changes include dependency updates and broad repository impact. |

## References

[1]: https://graphite.com/guides/code-review-github "How to do GitHub code reviews that don't take all week"
[pr2]: https://github.com/Cagatay342/openusage/pull/1 "Cagatay342/openusage#1 — Feat/openrouter aider config"
[pr3]: https://github.com/Gegcuk/QuizMaker/pull/756 "Gegcuk/QuizMaker#756 — fix(ai): reject duplicate generated questions"
[pr4]: https://github.com/JinnZ2/CEED/pull/2 "JinnZ2/CEED#2 — Claude/add claude documentation 0scrd"
[pr5]: https://github.com/Kirt22/Journal.IO-mono-repo/pull/70 "Kirt22/Journal.IO-mono-repo#70 — Codex"
[pr6]: https://github.com/attunehq/nudge/pull/72 "attunehq/nudge#72 — Add Cursor / cursor-agent hook support"
[pr7]: https://github.com/augentic/omnia-backends/pull/55 "augentic/omnia-backends#55 — Cursor fixes"
[pr8]: https://github.com/corosolto/client/pull/205 "corosolto/client#205 — docs: atribuição multiagente — AI generated & AI friendly"
[pr9]: https://github.com/ferrreo/local-image-detect-chrome/pull/7 "ferrreo/local-image-detect-chrome#7 — Restore OpenRouter-generated AI eval samples"
[pr10]: https://github.com/flatpark/flatpark/pull/211 "flatpark/flatpark#211 — feat(cursor): add Cursor, the AI code editor (co.anysphere.cursor)"
[pr11]: https://github.com/fwaris/FsHarness/pull/4 "fwaris/FsHarness#4 — Codex/vscode codex cli"
[pr12]: https://github.com/joangarvin/travseeker/pull/22 "joangarvin/travseeker#22 — Codex/sanitizers"
[pr13]: https://github.com/laurilehtinen/ccusage/pull/2 "laurilehtinen/ccusage#2 — feat(cursor): add Cursor CLI usage adapter"
[pr14]: https://github.com/powabase-ai/powabase-ai/pull/46 "powabase-ai/powabase-ai#46 — feat(copilot): project copilot + docs-RAG grounding"
[pr15]: https://github.com/springbrand-lab/springbrand-agent-setup/pull/13 "springbrand-lab/springbrand-agent-setup#13 — Codex/plan codex plugin distribution"
[pr16]: https://github.com/vshulcz/deja-vu/pull/396 "vshulcz/deja-vu#396 — aider: install target and a deja aider wrapper"
[pr17]: https://github.com/workcrewlabs/worker-pc-app/pull/45 "workcrewlabs/worker-pc-app#45 — Claude/like claude code"
[pr18]: https://github.com/xiaoqiuuuu/Codex-Pulse/pull/3 "xiaoqiuuuu/Codex-Pulse#3 — Codex/fix codex approval state"
[pr19]: https://github.com/ycoj/YCOJ/pull/18 "ycoj/YCOJ#18 — feat: add AI-generated test data"
