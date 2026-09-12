"""
modules/auth.py

Authentication and authorization helpers.

A user is authorized if they are an administrator or creator
of the configured Telegram channel.
"""

from __future__ import annotations

import requests

from modules.config import get_config
from modules.log import logger

_SESSION = requests.Session()


def is_admin(user_id: int) -> bool:
    """
    Check whether a Telegram user is an administrator
    of the configured Telegram channel.

    Parameters
    ----------
    user_id : int
        Telegram user ID.

    Returns
    -------
    bool
        True if the user is a creator or administrator.
    """

    config = get_config()

    bot_token = config["telegram"]["bot_token"]
    channel_id = config["telegram"]["channel_id"]

    url = (
        f"https://api.telegram.org/bot{bot_token}"
        f"/getChatMember"
    )

    try:

        response = _SESSION.get(
            url,
            params={
                "chat_id": channel_id,
                "user_id": user_id,
            },
            timeout=10,
        )

        response.raise_for_status()

        payload = response.json()

        if not payload.get("ok"):
            logger.warning(
                "getChatMember failed: %s",
                payload,
            )
            return False

        status = payload["result"]["status"]

        authorized = status in (
            "creator",
            "administrator",
        )

        logger.info(
            "Admin authentication. user_id=%s status=%s authorized=%s",
            user_id,
            status,
            authorized,
        )

        return authorized

    except requests.RequestException:

        logger.exception(
            "Unable to verify Telegram administrator."
        )

        return False
