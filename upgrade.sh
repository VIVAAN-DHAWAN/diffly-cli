#!/usr/bin/env sh
# upgrade.sh — one-shot upgrade for diffly-cli versions before 0.4.0
#
# This script upgrades an existing diffly-cli installation to the latest
# release (0.4.0+).  From 0.4.0 onwards, diffly has a built-in update
# mechanism (`diffly update`) and will prompt you when new versions are
# available, so this script is only needed once.
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/VIVAAN-DHAWAN/diffly-cli/main/upgrade.sh | sh
#
set -eu

DIFFLY_HOME="${DIFFLY_HOME:-${HOME}/.local/share/diffly-cli}"
DIFFLY_BIN="${DIFFLY_BIN:-${HOME}/.local/bin}"
DIFFLY_SOURCE="${DIFFLY_SOURCE:-git+https://github.com/VIVAAN-DHAWAN/diffly-cli.git}"

# ---------------------------------------------------------------
# Pre-flight checks
# ---------------------------------------------------------------

if ! command -v python3 >/dev/null 2>&1; then
  printf '%s\n' 'diffly-cli requires Python 3.10 or newer.' >&2
  exit 1
fi

if [ ! -d "${DIFFLY_HOME}" ]; then
  printf '%s\n' 'No existing diffly installation found.' >&2
  printf '%s\n' 'Use the install script instead:' >&2
  printf '%s\n' '  curl -fsSL https://raw.githubusercontent.com/VIVAAN-DHAWAN/diffly-cli/main/install.sh | sh' >&2
  exit 1
fi

# Show current version if possible.
if command -v diffly >/dev/null 2>&1; then
  CURRENT=$(diffly --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' || echo 'unknown')
  printf 'Upgrading diffly from %s…\n' "${CURRENT}"
else
  printf 'Upgrading diffly…\n'
fi

# ---------------------------------------------------------------
# Upgrade
# ---------------------------------------------------------------

printf 'Updating pip…\n'
"${DIFFLY_HOME}/bin/python" -m pip install --upgrade pip >/dev/null 2>&1 || true

printf 'Installing latest diffly from GitHub (this may take a minute)…\n'
"${DIFFLY_HOME}/bin/python" -m pip install --upgrade --progress-bar on "${DIFFLY_SOURCE}"

mkdir -p "${DIFFLY_BIN}"
ln -sf "${DIFFLY_HOME}/bin/diffly" "${DIFFLY_BIN}/diffly"
ln -sf "${DIFFLY_HOME}/bin/diffly" "${DIFFLY_BIN}/diffly-cli"

# ---------------------------------------------------------------
# Done
# ---------------------------------------------------------------

NEW=$(diffly --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' || echo 'latest')

printf '\n'
printf 'diffly upgraded to %s.\n' "${NEW}"
printf '\n'
printf 'From this version onwards, diffly will automatically check for updates\n'
printf 'every time you run it.  You can also run:\n'
printf '\n'
printf '  diffly update    — manually check for and install the latest release\n'
printf '  diffly doctor    — see your current update preference and diagnostics\n'
printf '\n'
