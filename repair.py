#!/usr/bin/env python3
"""Prüft Hermes Deutsch und spielt es bei Bedarf erneut ein."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def hermes_home() -> Path:
    value = os.environ.get("HERMES_HOME", "").strip()
    if value:
        return Path(value)
    if os.name == "nt":
        local = os.environ.get("LOCALAPPDATA", "").strip()
        return Path(local) / "hermes" if local else Path.home() / "AppData" / "Local" / "hermes"
    return Path.home() / ".hermes"


def configured_agent() -> Path:
    state = ROOT / "installed.json"
    try:
        return Path(json.loads(state.read_text())["agent_dir"])
    except Exception:
        return hermes_home() / "hermes-agent"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_wired(i18n: Path) -> bool:
    try:
        locale = re.search(r"^export type Locale = (.+)$", (i18n / "types.ts").read_text(), re.M)
        return bool(
            locale and "'de'" in locale.group(1)
            and "./de'" in (i18n / "catalog.ts").read_text()
            and "id: 'de'" in (i18n / "languages.ts").read_text()
            and (i18n / "de.ts").is_file()
            and sha256(i18n / "de.ts") == sha256(ROOT / "de.ts")
        )
    except OSError:
        return False


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent-dir", type=Path)
    parser.add_argument("--rebuild", action="store_true")
    args = parser.parse_args()
    agent = args.agent_dir or configured_agent()
    i18n = agent / "apps" / "desktop" / "src" / "i18n"
    if not i18n.is_dir():
        raise SystemExit(f"FEHLER: Hermes-i18n-Ordner nicht gefunden unter {agent}.")
    repaired = not is_wired(i18n)
    if repaired:
        result = subprocess.run([sys.executable, str(ROOT / "apply_de.py"), str(agent)], text=True)
        if result.returncode:
            raise SystemExit(result.returncode)
        stamp = hermes_home() / "desktop-build-stamp.json"
        if stamp.exists():
            stamp.unlink()
        print("Deutsch wurde erneut eingespielt.")
    else:
        print("Deutsch ist bereits aktuell; keine Änderung notwendig.")
    if args.rebuild and repaired:
        result = subprocess.run([sys.executable, "-m", "hermes_cli.main", "desktop", "--build-only", "--force-build"], cwd=agent)
        raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
