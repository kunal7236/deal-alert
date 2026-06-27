"""
modules/telegram.py

Wrapper around Telegram Bot API.

Responsibilities:
- Send messages
- Reply to incoming updates
- Register/Delete webhook

This module contains NO business logic.
"""

from __future__ import annotations

import time
from typing import Any

import requests

from modules.config import get_config
from modules.log import logger

# --------------------------------------------------------------------
# Persistent HTTP session
# --------------------------------------------------------------------

_session = requests.Session()

# --------------------------------------------------------------------
# Private helpers
# --------------------------------------------------------------------


def _base_url() -> str:
    """Return Telegram Bot API base URL."""
    token = get_config()["telegram"]["bot_token"]

    return f"https://api.telegram.org/bot{token}"


def _post(
    method: str,
    payload: dict[str, Any],
    timeout: int = 15,
) -> bool:
    """
    POST to Telegram Bot API.

    Retries:
        Attempt 1
        wait 1 second

        Attempt 2
        wait 2 seconds

        Attempt 3
        wait 4 seconds
    """

    retry_delays = [1, 2, 4]

    url = f"{_base_url()}/{method}"

    for attempt in range(len(retry_delays) + 1):

        try:

            response = _session.post(
                url,
                json=payload,
                timeout=timeout,
            )

            if response.ok:
                return True

            logger.warning(
                "Telegram API error. Method=%s Status=%s Body=%s",
                method,
                response.status_code,
                response.text,
            )

        except requests.RequestException:

            logger.exception(
                "Telegram request failed. Method=%s",
                method,
            )

        if attempt < len(retry_delays):
            time.sleep(retry_delays[attempt])

    logger.error(
        "Telegram request failed after retries. Method=%s",
        method,
    )

    return False


# --------------------------------------------------------------------
# Public API
# --------------------------------------------------------------------


def send_message(
    chat_id: int | str,
    text: str,
    disable_preview: bool = False,
) -> bool:
    """
    Send a Telegram message.

    Returns
    -------
    bool
        True if successfully sent.
    """

    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": disable_preview,
    }

    logger.info("Sending Telegram message to chat_id=%s", chat_id)

    return _post("sendMessage", payload)


def reply(
    update: dict[str, Any],
    text: str,
    disable_preview: bool = False,
) -> bool:
    """
    Reply to the chat from which the update originated.
    """

    chat_id = update["message"]["chat"]["id"]

    return send_message(
        chat_id=chat_id,
        text=text,
        disable_preview=disable_preview,
    )


def set_webhook(webhook_url: str) -> bool:
    """
    Register Telegram webhook.
    """

    secret = get_config()["telegram"]["webhook_secret"]

    payload = {
        "url": webhook_url,
        "secret_token": secret,
    }

    logger.info("Registering Telegram webhook.")

    return _post("setWebhook", payload)


def delete_webhook() -> bool:
    """
    Remove Telegram webhook.
    """

    logger.info("Deleting Telegram webhook.")

    return _post("deleteWebhook", {})


def get_webhook_info() -> dict[str, Any] | None:
    """
    Retrieve webhook information from Telegram.

    Useful for debugging.
    """

    try:

        response = _session.get(
            f"{_base_url()}/getWebhookInfo",
            timeout=15,
        )

        if response.ok:
            return response.json()

        logger.warning(
            "Unable to fetch webhook info. Status=%s",
            response.status_code,
        )

    except requests.RequestException:
        logger.exception("Failed to fetch webhook info.")

    return None