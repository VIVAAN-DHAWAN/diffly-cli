#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

RESULTS = Path("/tmp/diffly-benchmark-results.json")
OUT = Path("docs/benchmarks.md")

NOTES = {
    "Cagatay342/openusage#1": "BLOCK is well-supported: auth-store changes and a failed build/test check.",
    "Gegcuk/QuizMaker#756": "Likely conservative: the evidence includes new tests, but the heuristic still flags coverage on other changed production files.",
    "JinnZ2/CEED#2": "Possibly conservative: a very large mixed code/docs/experiment change with no reported checks.",
    "Kirt22/Journal.IO-mono-repo#70": "BLOCK is well-supported by auth-sensitive changes; unknown checks add a separate quarantine signal.",
    "attunehq/nudge#72": "Reasonable quarantine: dependency and broad hook/reference changes deserve review even though checks passed.",
    "augentic/omnia-backends#55": "Possibly conservative: a Cursor integration with dependency changes and passing checks was quarantined for coverage.",
    "corosolto/client#205": "Likely conservative: the PR is documentation/AI-attribution heavy, but package metadata and heuristic coverage rules fired.",
    "ferrreo/local-image-detect-chrome#7": "BLOCK is well-supported by a failed Chrome integration check; the asset-heavy diff also lacks obvious tests.",
    "flatpark/flatpark#211": "Likely conservative: packaging/registry assets are not naturally unit-tested, yet the coverage heuristic fired.",
    "fwaris/FsHarness#4": "Possibly conservative: editor cache artifacts and docs dominate the diff; checks were unavailable rather than failed.",
    "joangarvin/travseeker#22": "Potentially conservative on the auth flag because the evidence is stylesheet tokens; the final BLOCK also reflects the absence of obvious tests.",
    "laurilehtinen/ccusage#2": "Reasonable quarantine: dependency/schema changes and unavailable checks create a substantial review gate.",
    "powabase-ai/powabase-ai#46": "BLOCK is plausible: auth-sensitive tests and database migrations are both present, despite passing observed checks.",
    "springbrand-lab/springbrand-agent-setup#13": "Possibly conservative: this is largely agent/plugin documentation and workflow material with passing checks.",
    "vshulcz/deja-vu#396": "Likely conservative: Aider history and docs dominate; the heuristic treats the lack of nearby tests as a quarantine signal.",
    "workcrewlabs/worker-pc-app#45": "Reasonable quarantine: broad desktop changes, dependency metadata, and unavailable checks.",
    "xiaoqiuuuu/Codex-Pulse#3": "Reasonable quarantine: test-script dependency changes and broad Rust/Tauri changes merit review.",
    "ycoj/YCOJ#18": "Reasonable quarantine: AI-generation changes include dependency updates and broad repository impact.",
}


def fmt_minutes(value: float) -> str:
    if value >= 60:
        return f"{value / 60:.1f} h"
    return f"{value:.1f} min"


def main() -> None:
    rows = json.loads(RESULTS.read_text())
    counts = Counter(row.get("verdict", "ERROR") for row in rows)
    flagged = sum(counts[v] for v in ("QUARANTINE", "BLOCK"))
    total_lines = sum(row.get("lines", 0) for row in rows)
    total_raw = sum(row.get("raw_minutes", 0) for row in rows)
    total_diffly = sum(row.get("diffly_minutes", 0) for row in rows)
    average_reduction = (1 - total_diffly / total_raw) * 100 if total_raw else 0

    out = [
        "# Benchmark: agent-sized public pull requests",
        "",
        f"Across **{len(rows)} recent public pull requests** selected for visible Claude, Codex, Copilot, Cursor, Aider, Devin, or AI-generated attribution and large diffs, Diffly retrospectively flagged **{flagged}/{len(rows)}** of these merged PRs as requiring a gate: {counts['BLOCK']} BLOCK and {counts['QUARANTINE']} QUARANTINE; {counts['SHIP']} were SHIP. The sample contains **{total_lines:,} changed lines**; under the stated proxy, the raw-diff reading estimate is **{fmt_minutes(total_raw)}** versus **{fmt_minutes(total_diffly)}** for the compact Diffly output, a modeled reduction of **{average_reduction:.0f}%**, not an observed timing study.",
        "",
        "The selection is deliberately discovery-biased toward PRs whose title or searchable body names an AI coding tool, so it is evidence about agent-sized, agent-attributed changes—not a prevalence estimate for all GitHub pull requests. The table preserves cases where the deterministic rules look conservative or potentially wrong instead of treating every flag as a success.",
        "",
        "**Reading-time proxy.** A changed line is treated as one unit of review effort at **300 changed lines/hour (5/minute)**, with **one additional minute per changed file** for navigation and context switching. Diffly is modeled as **two minutes plus 10 seconds per changed file** for reading its compact summary output. These are transparent planning assumptions, not measurements; the file-count term is included because code-review guidance consistently treats smaller, more focused PRs as easier to review [1].",
        "",
        "| Public PR | Primary language | Size | Diffly verdict | Risk flags caught | Raw diff vs. Diffly | Honest read |",
        "| --- | --- | ---: | --- | --- | ---: | --- |",
    ]
    for index, row in enumerate(rows, start=2):
        key = f"{row['repo']}#{row['number']}"
        flags = ", ".join(f"`{flag['code']}`" for flag in row.get("flags", [])) or "—"
        size = f"{row['files']} files / +{row['additions']}/-{row['deletions']}"
        times = f"{fmt_minutes(row['raw_minutes'])} / {fmt_minutes(row['diffly_minutes'])}"
        note = NOTES.get(key, "No additional manual caveat recorded.")
        out.append(
            f"| [{key}][pr{index}] | {row.get('language', 'Unknown')} | {size} | **{row['verdict']}** | {flags} | {times} | {note} |"
        )

    out += [
        "",
        "## References",
        "",
        "[1]: https://graphite.com/guides/code-review-github \"How to do GitHub code reviews that don't take all week\"",
    ]
    for index, row in enumerate(rows, start=2):
        out.append(f"[pr{index}]: {row['url']} \"{row['repo']}#{row['number']} — {row['title'].replace(chr(34), '')}\"")
    OUT.write_text("\n".join(out) + "\n")
    print(f"Wrote {OUT} with {len(rows)} rows")


if __name__ == "__main__":
    main()
