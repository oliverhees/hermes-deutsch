#!/usr/bin/env python3
"""Installiert Hermes Deutsch als lokalen, rücknehmbaren Kompatibilitäts-Patch."""
from __future__ import annotations

import argparse
import json
import os
import shutil
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


def run(command: list[str]) -> None:
    result = subprocess.run(command, text=True)
    if result.returncode:
        raise SystemExit(result.returncode)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent-dir", type=Path, help="Pfad zum Hermes-Agent-Checkout")
    parser.add_argument("--no-build", action="store_true", help="Desktop-Neubau überspringen")
    args = parser.parse_args()

    home = hermes_home()
    agent = args.agent_dir or home / "hermes-agent"
    state = home / "hermes-deutsch"
    hook_dir = home / "hooks" / "hermes-deutsch"
    if not (agent / "apps" / "desktop" / "src" / "i18n").is_dir():
        raise SystemExit(f"FEHLER: Hermes-i18n-Ordner nicht gefunden unter {agent}. Nutze bei Bedarf --agent-dir.")

    state.mkdir(parents=True, exist_ok=True)
    for name in ("de.ts", "apply_de.py", "restore_original.py", "repair.py", "uninstall.py"):
        shutil.copy2(ROOT / name, state / name)
    (state / "installed.json").write_text(json.dumps({"agent_dir": str(agent)}, indent=2) + "\n")

    hook_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / "hook" / "HOOK.yaml", hook_dir / "HOOK.yaml")
    shutil.copy2(ROOT / "hook" / "handler.py", hook_dir / "handler.py")

    print("Installiere deutsche Sprachdatei …")
    run([sys.executable, str(state / "apply_de.py"), str(agent)])
    if not args.no_build:
        print("Baue Hermes Desktop neu …")
        run([sys.executable, "-m", "hermes_cli.main", "desktop", "--build-only", "--force-build"])
    print("\nFertig. Hermes Deutsch ist installiert.")
    print("Der Gateway-Hook prüft nach Gateway-Starts auf entfernte Dateien.")
    print("Für einen reinen Desktop-Update ohne Gateway: python3 ~/.hermes/hermes-deutsch/repair.py --rebuild")


if __name__ == "__main__":
    main()
