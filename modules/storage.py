"""
modules/storage.py

JSON storage utilities.

Responsibilities:
- Atomic JSON writes
- JSON reads
- Ensure files exist
- Seen database helpers
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from modules.constants import DATA_DIR
from modules.log import logger

# ---------------------------------------------------------------------
# Seen database
# ---------------------------------------------------------------------

_SEEN_FILE = DATA_DIR / "seen.json"


# ---------------------------------------------------------------------
# Generic JSON Helpers
# ---------------------------------------------------------------------


def ensure_file(path: Path, default_data: Any) -> None:
    """
    Create a file with default data if it does not exist.
    """

    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        return

    save_json(path, default_data)


def load_json(path: Path) -> Any:
    """
    Load JSON file.
    """

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(path: Path, data: Any) -> None:
    """
    Atomically save JSON.
    """

    path.parent.mkdir(parents=True, exist_ok=True)

    temp_path = path.with_suffix(path.suffix + ".tmp")

    with open(temp_path, "w", encoding="utf-8") as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False,
        )

        file.flush()

        os.fsync(file.fileno())

    os.replace(temp_path, path)


# ---------------------------------------------------------------------
# Seen Helpers
# ---------------------------------------------------------------------


def load_seen() -> set[str]:
    """
    Load seen PID database.
    """

    ensure_file(_SEEN_FILE, [])

    data = load_json(_SEEN_FILE)

    return set(data)


def save_seen(pids: set[str]) -> None:
    """
    Save current seen PID database.
    """

    save_json(
        _SEEN_FILE,
        sorted(pids),
    )