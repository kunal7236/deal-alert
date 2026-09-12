"""
webhook.py

FastAPI application that receives Telegram webhook updates.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi import Header
from fastapi import HTTPException
from fastapi import Request

from modules.commands import dispatch
from modules.config import get_config, reload_config
from modules.log import logger

reload_config()

app = FastAPI(
    title="Deal Alert Webhook",
    version="1.0.0",
)


@app.get("/")
async def root():
    """
    Health check endpoint.
    """

    return {
        "status": "ok",
        "service": "Deal Alert Webhook",
    }


@app.post("/webhook")
async def webhook(
    request: Request,
    x_telegram_bot_api_secret_token: str | None = Header(default=None),
):
    """
    Telegram webhook endpoint.
    """

    config = get_config()

    expected_secret = config["telegram"]["webhook_secret"]

    if x_telegram_bot_api_secret_token != expected_secret:

        logger.warning(
            "Invalid webhook secret received."
        )

        raise HTTPException(
            status_code=403,
            detail="Forbidden",
        )

    update = await request.json()

    try:

        dispatch(update)

    except Exception:

        logger.exception(
            "Unhandled exception while processing update."
        )

    return {
        "ok": True,
    }
