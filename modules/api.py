"""
modules/api.py

Deals API client.

Responsibilities:
- Fetch latest deals
- Validate API response
- Return deal list

This module contains NO business logic.
"""

from __future__ import annotations

from typing import Any

import requests

from modules.config import get_config
from modules.exceptions import ApiError
from modules.log import logger

# ---------------------------------------------------------------------
# Persistent HTTP session
# ---------------------------------------------------------------------

_session = requests.Session()

DEFAULT_TIMEOUT = 20


# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------


def fetch_deals() -> list[dict[str, Any]]:
    """
    Fetch latest deals from the configured API.

    Returns
    -------
    list[dict]

    Raises
    ------
    ApiError
        If request fails or response is invalid.
    """

    url = get_config()["api"]["url"]

    logger.info("Fetching deals from API.")

    try:

        response = _session.get(
            url,
            timeout=DEFAULT_TIMEOUT,
        )

    except requests.RequestException as exc:

        raise ApiError(
            f"Unable to reach Deals API: {exc}"
        ) from exc

    if response.status_code != 200:

        raise ApiError(
            f"Unexpected HTTP status: {response.status_code}"
        )

    try:

        payload = response.json()

    except ValueError as exc:

        raise ApiError(
            "API returned invalid JSON."
        ) from exc

    if not isinstance(payload, dict):

        raise ApiError(
            "Expected JSON object."
        )

    deals = payload.get("deals")

    if deals is None:

        raise ApiError(
            "Missing 'deals' field."
        )

    if not isinstance(deals, list):

        raise ApiError(
            "'deals' is not a list."
        )

    logger.info(
        "Received %s deals.",
        len(deals),
    )

    return deals