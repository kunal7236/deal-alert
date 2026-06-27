"""
modules/matcher.py

Keyword matching.

Responsibilities:
- Load configured search keywords.
- Perform case-insensitive substring matching.
- Return matched keyword.
"""

from __future__ import annotations

from modules.config import get_config

# ---------------------------------------------------------------------
# Module Cache
# ---------------------------------------------------------------------

_keywords: list[str] = []


# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------


def reload_keywords() -> None:
    """
    Reload keywords from configuration.

    Should be called whenever config.json is reloaded.
    """

    global _keywords

    config = get_config()

    _keywords = [
        keyword.lower().strip()
        for keyword in config["search_keys"]
    ]


def match_deal(deal: dict) -> str | None:
    """
    Match a deal against configured keywords.

    Parameters
    ----------
    deal : dict

    Returns
    -------
    str | None

    Returns the matched keyword if found,
    otherwise None.
    """

    title = deal.get("title", "")

    if not title:
        return None

    title = title.lower()

    for keyword in _keywords:

        if keyword in title:
            return keyword

    return None


def get_keywords() -> list[str]:
    """
    Return currently loaded keywords.
    """

    return _keywords.copy()