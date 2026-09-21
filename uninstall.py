#!/usr/bin/env python3
"""Entfernt Hermes Deutsch und stellt die gesicherten Hermes-Originale wieder her."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def hermes_home() -> Path:
    value = os.environ.get("HERMES_HOME", "").strip()
    if value:
        return Path(value)
    if os.name == "nt":
        local = os.environ.get("LOCALAPPDATA", "").strip()
        return Path(local) / "hermes" if local else Path.home() / "AppData" / "Local" / "hermes"
    return Path.home() / ".hermes"


def main() -> None:
    home = hermes_home()
    state = home / "hermes-deutsch"
    try:
        agent = Path(json.loads((state / "installed.json").read_text())["agent_dir"])
    except Exception:
        agent = home / "hermes-agent"
    restore = state / "restore_original.py"
    if not restore.is_file():
        raise SystemExit(f"FEHLER: Installationsdaten fehlen unter {state}; keine Änderung vorgenommen.")
    result = subprocess.run([sys.executable, str(restore), str(agent)], text=True)
    if result.returncode:
        raise SystemExit(result.returncode)
    shutil.rmtree(home / "hooks" / "hermes-deutsch", ignore_errors=True)
    shutil.rmtree(state, ignore_errors=True)
    print("Hermes Deutsch wurde entfernt. Starte Hermes Desktop neu.")


if __name__ == "__main__":
    main()
