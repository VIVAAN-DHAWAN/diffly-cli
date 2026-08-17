# Authentic visual verification

The previous screenshot assets were synthetic terminal-style compositions and have been replaced.

New assets are generated from ANSI transcripts captured by the Unix `script` command while running the real CLI against these public pull requests:

- `microsoft/vscode#330848`
- `kubernetes/kubernetes#141413`
- `astral-sh/ruff#27808`

The verified Ruff screenshot visibly contains the actual command `$ diffly-cli pr astral-sh/ruff 27808 --output ...`, the real report URL, title, commit/file/line counts, `BLOCK` verdict, failed check evidence, and `NO_TEST_COVERAGE` evidence. The GIF is composed only of frames rendered from these captured transcripts; no synthetic demo copy is used.

Verified on 2026-08-17.
