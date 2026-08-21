# Security Policy

## Supported versions

| Version | Supported |
| --- | --- |
| latest release | yes |
| older releases | no |

## Reporting a vulnerability

Report security issues privately through [GitHub's security advisory form](https://github.com/VIVAAN-DHAWAN/diffly-cli/security/advisories/new), not a public issue. Include reproduction steps, affected versions, and any relevant logs with secrets redacted.

## What matters most in this codebase

- **Token handling:** `diffly` reads `GITHUB_TOKEN` from the environment or the Action context. Tokens are never logged, echoed, or included in reports.
- **LLM boundary:** deterministic mode sends no code anywhere. With `--explain`, bounded, secret-redacted context is sent to the configured OpenAI-compatible endpoint. Model output is strictly validated and cannot change verdicts. See [`docs/phase-2-contract.md`](docs/phase-2-contract.md).
- **Untrusted input:** PR titles, bodies, diffs, and check names are treated as data, never instructions.

Please review [`docs/phase-2-contract.md`](docs/phase-2-contract.md) before enabling `--explain` for sensitive repositories.
