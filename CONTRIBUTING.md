# Contributing to diffly

Thanks for helping make pull-request triage deterministic. This guide covers what you need to get productive quickly.

## Development setup

```bash
git clone https://github.com/VIVAAN-DHAWAN/diffly-cli.git
cd diffly-cli
python -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[dev]'
pytest -q
```

The CI matrix runs the suite on Python 3.10 through 3.13.

## Ground rules

- **Determinism is the product.** The same PR data must always produce the same flags and verdict. Never let heuristics, network state, or LLM prose change a verdict.
- **Fail closed.** When evidence is missing (truncated tree, unavailable checks), quarantine rather than assume success.
- **Keep the LLM sandboxed.** Generated explanations are clearly labeled, validated against a strict contract, redacted, and cannot influence `PASS`, `QUARANTINE`, or `BLOCK`. See [`docs/phase-2-contract.md`](docs/phase-2-contract.md).
- **Focused changes.** One behavior change per pull request, with regression tests.

## Pull-request checklist

1. Add or update tests for any behavior change.
2. Run `pytest -q` locally.
3. Update [`CHANGELOG.md`](CHANGELOG.md) under **Unreleased**.
4. If you changed user-facing behavior, update the README section that documents it.
5. Verify any new example commands against live public repositories — broken examples are bugs.

## Reporting bugs

Open an issue with the command you ran, the full output, your OS and Python version, and the repository/PR analyzed (public ones only). Run `diffly doctor` and include its output for environment problems.

## Security

Do not open public issues for security reports. Use [GitHub's security advisory form](https://github.com/VIVAAN-DHAWAN/diffly-cli/security/advisories/new). See [`SECURITY.md`](SECURITY.md).
