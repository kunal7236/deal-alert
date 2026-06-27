"""
modules/stats.py

Daily statistics.

Maintains stats.json which is used by report.py.
"""

from __future__ import annotations

from modules.constants import DATA_DIR
from modules.storage import load_json, save_json

_STATS_FILE = DATA_DIR / "stats.json"


def get_stats() -> dict:
    """
    Return current statistics.
    """

    return load_json(_STATS_FILE)


def increment_run() -> None:
    """
    Increment successful monitor runs.
    """

    stats = get_stats()

    stats["runs"] += 1

    save_json(_STATS_FILE, stats)


def increment_matches(count: int) -> None:
    """
    Increment keyword match count.
    """

    if count <= 0:
        return

    stats = get_stats()

    stats["matches"] += count

    save_json(_STATS_FILE, stats)


def reset_stats() -> None:
    """
    Reset daily statistics.
    """

    save_json(
        _STATS_FILE,
        {
            "runs": 0,
            "matches": 0,
        },
    )