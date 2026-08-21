#!/usr/bin/env bash
set -euo pipefail

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
CAPTURE_DIR="$ROOT/assets/real-captures"
mkdir -p "$CAPTURE_DIR"

run_capture() {
  name="$1"
  repo="$2"
  number="$3"
  report="/tmp/diffly-${name}.md"
  rm -f "$report"
  session_cmd="cd \"$ROOT\" && printf '\\033[1;32m$ diffly-cli pr $repo $number --output $report\\033[0m\\n' && diffly-cli pr $repo $number --output $report && printf '\\n\\033[1;32m$ head -34 $report\\033[0m\\n' && head -34 \"$report\""
  COLUMNS=140 LINES=46 script -q -e -c "$session_cmd" "$CAPTURE_DIR/${name}.ansi" >/dev/null
}

run_capture vscode-330848 microsoft/vscode 330848
run_capture kubernetes-141413 kubernetes/kubernetes 141413
run_capture ruff-27808 astral-sh/ruff 27808
printf '%s\n' "Captured real terminal sessions in $CAPTURE_DIR"
