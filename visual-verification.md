# Authentic visual verification

The committed demo assets are generated from ANSI transcripts captured by the Unix `script` command while running the real CLI against these public pull requests:

- `microsoft/vscode#330848`
- `kubernetes/kubernetes#141413`
- `astral-sh/ruff#27808`

The refreshed captures show the current live metadata and verdicts: VS Code has 25 files and +2,557/-251 lines with `QUARANTINE`; Kubernetes has 41 files and +708/-740 lines with `QUARANTINE` and a pending `tide` check; Ruff has 53 files and +1,845/-274 lines across 4 commits with `BLOCK` because `CodSpeed Performance Analysis` failed. The screenshots and GIF are rendered only from these captured transcripts; no synthetic demo copy is used.

Verified on 2026-08-18.
