"""Gateway-Hook für Hermes Deutsch. Fehler dürfen den Gateway-Start nie stoppen."""
import os
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


async def handle(event_type: str, context: dict):
    repair = hermes_home() / "hermes-deutsch" / "repair.py"
    if repair.is_file():
        try:
            subprocess.Popen([sys.executable, str(repair), "--rebuild"], start_new_session=True)
        except OSError:
            pass
