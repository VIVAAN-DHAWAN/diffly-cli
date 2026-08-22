#!/usr/bin/env sh
set -eu

DIFFLY_HOME="${DIFFLY_HOME:-${HOME}/.local/share/diffly-cli}"
DIFFLY_BIN="${DIFFLY_BIN:-${HOME}/.local/bin}"
DIFFLY_SOURCE="${DIFFLY_SOURCE:-git+https://github.com/VIVAAN-DHAWAN/diffly-cli.git}"

if ! command -v python3 >/dev/null 2>&1; then
  printf '%s\n' 'diffly-cli requires Python 3.10 or newer.' >&2
  exit 1
fi

python3 -m venv "${DIFFLY_HOME}"
"${DIFFLY_HOME}/bin/python" -m pip install --upgrade pip >/dev/null 2>&1 || true
printf 'Installing diffly-cli (this may take a minute)…\n'
"${DIFFLY_HOME}/bin/python" -m pip install --upgrade --progress-bar on "${DIFFLY_SOURCE}"
mkdir -p "${DIFFLY_BIN}"
ln -sf "${DIFFLY_HOME}/bin/diffly" "${DIFFLY_BIN}/diffly"
# Keep the old executable as a compatibility alias for existing scripts.
ln -sf "${DIFFLY_HOME}/bin/diffly" "${DIFFLY_BIN}/diffly-cli"

printf '\nInstalled diffly.\n'
printf 'Run: diffly pr <owner/repo> <pr-number>\n'
case ":${PATH}:" in
  *":${DIFFLY_BIN}:"*) ;;
  *) printf 'If the command is not found, add %s to PATH.\n' "${DIFFLY_BIN}" ;;
esac
