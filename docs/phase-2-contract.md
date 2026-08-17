# Phase 2 contract

## Scope

Phase 2 adds an optional literate-diff explainer on top of the deterministic Phase 1 triage engine. It explains the change in review order—background, intent, narrative steps, and review questions—without changing the deterministic verdict.

## Model access

The default model is `gpt-5-mini`, selected from the live catalog on 2026-08-17 because it is the catalog’s cost-aware structured-analysis workhorse. The implementation is provider-neutral through an OpenAI-compatible endpoint. It accepts `DIFFLY_LLM_API_KEY`, `DIFFLY_LLM_BASE_URL`, and `DIFFLY_LLM_MODEL`; when those are absent, it can fall back to `OPENAI_API_KEY`, `OPENAI_API_BASE`, and `DIFFLY_LLM_MODEL` for the built-in proxy or another compatible environment.

No credential is stored in the repository, embedded in prompts, or printed in reports. The explainer is opt-in through `--explain` so deterministic triage remains usable without an LLM.

## Fact boundary

Facts returned directly by GitHub and computed deterministically remain in the existing report sections. Generated prose is clearly labeled under `## Literate diff — generated explanation`. The model is instructed that it cannot override `SHIP`, `QUARANTINE`, or `BLOCK`; its output is explanatory only.

## Redaction boundary

Before model input, the tool redacts GitHub tokens, private keys, AWS-style access keys, bearer tokens, common secret assignments, and high-entropy secret-like values. Redaction is conservative and visible in the local run summary as a count, not as the original value.

## Structured output

The model must return strict JSON with: `background`, `intent`, `narrative`, `review_questions`, and `uncertainties`. Each narrative step includes a title, affected files, explanation, evidence, and an optional short code snippet. Invalid JSON, schema mismatch, empty required prose, or an API failure causes a safe fallback: deterministic triage is still printed and the generated section is omitted with an error note.

## Context limits

The explainer receives PR metadata, deterministic flags and verdict, changed-file facts, and bounded redacted patches. It does not receive the entire repository or unbounded diffs. The default total prompt context is capped by characters, and each file patch is capped independently.

## Testing target

Phase 2 is complete only when redaction, schema validation, prompt construction, API failure fallback, deterministic-verdict immutability, CLI integration, and at least one live public pull-request explanation are verified.
