"""Check for and install updates to diffly-cli.

Version checks use the PyPI JSON API so the lookup is fast and does not
require git or GitHub API authentication.  The actual upgrade command is
chosen based on how diffly was originally installed:

- ``curl | install.sh``  → re-runs the install script
- ``brew install``       → runs ``brew upgrade diffly-cli``
- ``pip install``        → runs ``pip install --upgrade diffly-cli``
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

from . import __version__

CONFIG_DIR = Path.home() / ".diffly"
CONFIG_FILE = CONFIG_DIR / "config.json"
PYPI_URL = "https://pypi.org/pypi/diffly-cli/json"
INSTALL_SCRIPT_URL = (
    "https://raw.githubusercontent.com/VIVAAN-DHAWAN/diffly-cli/main/install.sh"
)
INSTALLER_VENV = Path.home() / ".local" / "share" / "diffly-cli"


# ---------------------------------------------------------------------------
# Version helpers
# ---------------------------------------------------------------------------

def _parse_version(version_str: str) -> tuple[int, ...]:
    """Parse a version string like '0.3.0' into a comparable tuple."""
    return tuple(int(part) for part in version_str.split(".") if part.isdigit())


# ---------------------------------------------------------------------------
# Config persistence  (~/.diffly/config.json)
# ---------------------------------------------------------------------------

def _load_config() -> dict[str, Any]:
    """Load the diffly user configuration, returning defaults when absent."""
    if not CONFIG_FILE.exists():
        return {}
    try:
        return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def _save_config(config: dict[str, Any]) -> None:
    """Persist diffly user configuration to disk."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(config, indent=2), encoding="utf-8")


def get_update_preference() -> str | None:
    """Return the stored update preference: 'auto', 'manual', or None if never set."""
    return _load_config().get("update_preference")


def set_update_preference(preference: str) -> None:
    """Persist the user's update preference ('auto' or 'manual')."""
    config = _load_config()
    config["update_preference"] = preference
    _save_config(config)


# ---------------------------------------------------------------------------
# PyPI lookup
# ---------------------------------------------------------------------------

def _fetch_pypi_info() -> dict[str, Any] | None:
    """Fetch the latest release metadata from PyPI."""
    import urllib.request
    import urllib.error

    try:
        req = urllib.request.Request(PYPI_URL, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, OSError, json.JSONDecodeError):
        return None


def check_for_update() -> str | None:
    """Return the latest version string if a newer release exists on PyPI.

    Returns ``None`` when the installed version is current or when the PyPI
    lookup cannot be completed (network error, timeout, etc.).
    """
    info = _fetch_pypi_info()
    if info is None:
        return None
    try:
        latest = info["info"]["version"]
    except (KeyError, TypeError):
        return None
    if _parse_version(latest) > _parse_version(__version__):
        return latest
    return None


# ---------------------------------------------------------------------------
# Installation detection
# ---------------------------------------------------------------------------

def _detect_install_method() -> str:
    """Return 'installer', 'brew', or 'pip' based on how diffly was installed."""
    if INSTALLER_VENV.is_dir():
        return "installer"
    if shutil.which("brew") is not None:
        try:
            result = subprocess.run(
                ["brew", "list", "diffly-cli"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode == 0:
                return "brew"
        except (subprocess.TimeoutExpired, OSError):
            pass
    return "pip"


# ---------------------------------------------------------------------------
# Update installation
# ---------------------------------------------------------------------------

def install_update() -> bool:
    """Upgrade diffly using the same method it was originally installed with.

    Detects whether diffly was installed via the curl installer script,
    Homebrew, or pip, and runs the matching upgrade command.
    """
    method = _detect_install_method()

    if method == "installer":
        cmd = f"curl -fsSL {INSTALL_SCRIPT_URL} | sh"
        args = ["sh", "-c", cmd]
    elif method == "brew":
        args = ["brew", "upgrade", "diffly-cli"]
    else:
        args = [sys.executable, "-m", "pip", "install", "--upgrade", "diffly-cli"]

    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=120,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, OSError):
        return False