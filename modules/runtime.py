"""
modules/runtime.py

Runtime information.

Maintains the latest monitor execution state.
"""

from __future__ import annotations

from modules.storage import load_json, save_json
from modules.utils import current_ist_time
from modules import constants

_RUNTIME_FILE = constants.DATA_DIR / "runtime.json"


def get_runtime() -> dict:
    """
    Return current runtime information.
    """

    return load_json(_RUNTIME_FILE)


def update_runtime(
    *,
    status: str,
    api_response_ms: int | None,
    deals_received: int,
    keyword_matches: int,
    notifications_sent: int,
) -> None:
    """
    Update runtime.json.
    """

    runtime = {
        "last_run": current_ist_time(),
        "last_status": status,
        "api_response_ms": api_response_ms,
        "deals_received": deals_received,
        "keyword_matches": keyword_matches,
        "notifications_sent": notifications_sent,
    }

    save_json(_RUNTIME_FILE, runtime)