#!/usr/bin/env sh
set -eu

DIFFLY_HOME="${DIFFLY_HOME:-${HOME}/.local/share/diffly-cli}"
DIFFLY_BIN="${DIFFLY_BIN:-${HOME}/.local/bin}"
DIFFLY_SOURCE="${DIFFLY_SOURCE:-git+https://github.com/VIVAAN-DHAWAN/diffly-cli.git}"

if ! command -v python3 >/dev/null 2>&1; then
  printf '%s\n' 'Error: python3 is required but not found in PATH.' >&2
  exit 1
fi

py_version=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
if ! python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)'; then
  printf '%s\n' "Error: diffly-cli requires Python 3.10 or newer, found ${py_version}." >&2
  exit 1
fi

if ! command -v git >/dev/null 2>&1; then
  printf '%s\n' 'Error: git is required but not found in PATH.' >&2
  exit 1
fi

if ! python3 -m venv --help >/dev/null 2>&1; then
  printf '%s\n' 'Error: python3-venv is required but not installed.' >&2
  exit 1
fi

if ! mkdir -p "${DIFFLY_HOME}"; then
  printf '%s\n' "Error: Cannot create directory ${DIFFLY_HOME}. Check permissions." >&2
  exit 1
fi

if ! mkdir -p "${DIFFLY_BIN}"; then
  printf '%s\n' "Error: Cannot create directory ${DIFFLY_BIN}. Check permissions." >&2
  exit 1
fi

printf 'Setting up virtual environment...\n'
python3 -m venv "${DIFFLY_HOME}"

printf 'Installing diffly-cli...\n'
if ! "${DIFFLY_HOME}/bin/python" -m pip install --upgrade pip; then
  printf '%s\n' 'Error: Failed to upgrade pip. See output above.' >&2
  exit 1
fi

if ! "${DIFFLY_HOME}/bin/python" -m pip install --upgrade "${DIFFLY_SOURCE}"; then
  printf '%s\n' 'Error: Failed to install diffly-cli. See output above.' >&2
  exit 1
fi

ln -sf "${DIFFLY_HOME}/bin/diffly-cli" "${DIFFLY_BIN}/diffly-cli"

printf '\nInstalled diffly-cli.\n'
printf 'Run: diffly-cli pr <owner/repo> <pr-number>\n'
case ":${PATH}:" in
  *":${DIFFLY_BIN}:"*) ;;
  *) printf 'If the command is not found, add %s to PATH.\n' "${DIFFLY_BIN}" ;;
esac
