"""
modules/commands.py

Telegram command dispatcher.
"""

from __future__ import annotations

from typing import Callable

from modules.auth import is_admin
from modules.config import (
    get_config,
    reload_config,
    save_config,
)
from modules.cron import update_monitor_frequency
from modules.matcher import reload_keywords
from modules.runtime import get_runtime
from modules.telegram import reply
from modules.log import logger


# ----------------------------------------------------------------------
# Command Handlers
# ----------------------------------------------------------------------


def help_command(update: dict, args: list[str]) -> None:

    message = (
        "Deal Alert Bot\n\n"
        "Available Commands:\n\n"
        "/help\n"
        "/status\n"
        "/reload\n"
        "/showSearchList\n"
        "/addToList <keyword>\n"
        "/removeFromList <keyword>\n"
        "/setFrequency <minutes>"
    )

    reply(update, message)


def status_command(update: dict, args: list[str]) -> None:

    config = get_config()
    runtime = get_runtime()

    message = (
        "📊 <b>Deal Alert Status</b>\n\n"
        f"Frequency : {config['frequency']} min\n"
        f"Keywords : {len(config['search_keys'])}\n\n"
        f"Last Run : {runtime['last_run']}\n"
        f"Last Status : {runtime['last_status']}\n"
        f"API Response : {runtime['api_response_ms']} ms\n"
        f"Deals Received : {runtime['deals_received']}\n"
        f"Keyword Matches : {runtime['keyword_matches']}\n"
        f"Notifications Sent : {runtime['notifications_sent']}"
    )

    reply(update, message)


def reload_command(update: dict, args: list[str]) -> None:

    reload_config()
    reload_keywords()

    reply(update, "Configuration reloaded.")


def show_search_list_command(update: dict, args: list[str]) -> None:

    keywords = get_config()["search_keys"]

    if not keywords:
        reply(update, "Search list is empty.")
        return

    message = "Search Keywords\n\n"

    for index, keyword in enumerate(keywords, start=1):
        message += f"{index}. {keyword}\n"

    reply(update, message)


def add_to_list_command(update: dict, args: list[str]) -> None:

    if not args:
        reply(update, "Usage:\n/addToList <keyword>")
        return

    keyword = " ".join(args).strip()

    config = get_config()

    if keyword in config["search_keys"]:
        reply(update, "Keyword already exists.")
        return

    config["search_keys"].append(keyword)

    save_config(config)
    reload_keywords()

    reply(update, f"Added '{keyword}'.")


def remove_from_list_command(update: dict, args: list[str]) -> None:

    if not args:
        reply(update, "Usage:\n/removeFromList <keyword>")
        return

    keyword = " ".join(args).strip()

    config = get_config()

    if keyword not in config["search_keys"]:
        reply(update, "Keyword not found.")
        return

    config["search_keys"].remove(keyword)

    save_config(config)
    reload_keywords()

    reply(update, f"Removed '{keyword}'.")


def set_frequency_command(update: dict, args: list[str]) -> None:

    if len(args) != 1:
        reply(update, "Usage:\n/setFrequency <minutes>")
        return

    try:
        minutes = int(args[0])
    except ValueError:
        reply(update, "Frequency must be an integer.")
        return

    if minutes < 1 or minutes > 59:
        reply(update, "Frequency must be between 1 and 59 minutes.")
        return

    config = get_config()

    config["frequency"] = minutes

    save_config(config)

    update_monitor_frequency(minutes)

    reply(
        update,
        f"Frequency updated to {minutes} minute(s).",
    )


# ----------------------------------------------------------------------
# Registry
# ----------------------------------------------------------------------

COMMANDS: dict[str, Callable[[dict, list[str]], None]] = {
    "help": help_command,
    "status": status_command,
    "reload": reload_command,
    "showsearchlist": show_search_list_command,
    "addtolist": add_to_list_command,
    "removefromlist": remove_from_list_command,
    "setfrequency": set_frequency_command,
}


# ----------------------------------------------------------------------
# Dispatcher
# ----------------------------------------------------------------------


def dispatch(update: dict) -> None:

    message = update.get("message")

    if message is None:
        return

    text = message.get("text", "")

    if not text.startswith("/"):
        return

    user_id = message["from"]["id"]

    if not is_admin(user_id):
        logger.warning(
            "Unauthorized access by user_id=%s",
            user_id,
        )
        return

    parts = text.split()

    command = parts[0][1:].split("@")[0].lower()

    args = parts[1:]

    handler = COMMANDS.get(command)

    if handler is None:
        reply(
            update,
            "Unknown command.\nUse /help",
        )
        return

    logger.info(
        "Executing command '%s'",
        command,
    )

    try:
        handler(update, args)

    except Exception:
        logger.exception(
            "Command '%s' failed.",
            command,
        )

        reply(
            update,
            "Internal server error.",
        )