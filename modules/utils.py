"""
modules/utils.py

Common utility functions.
"""

from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")


def current_ist_time() -> str:
    """
    Return current time in IST.

    Format:
        YYYY-MM-DD HH:MM:SS
    """

    return datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S")