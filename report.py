"""
report.py

Daily report entry point.
Executed by cron every day at 2:00 PM IST.
"""

from __future__ import annotations

from modules.config import get_config, reload_config
from modules.log import logger
from modules.stats import get_stats, reset_stats
from modules.telegram import send_message


def main() -> None:

    logger.info("========== Daily Report Started ==========")

    reload_config()

    stats = get_stats()

    channel_id = get_config()["telegram"]["channel_id"]

    message = (
        "📊 <b>Deal Alert Daily Report</b>\n\n"
        f"Total Runs : {stats['runs']}\n"
        f"Total Keyword Matches : {stats['matches']}"
    )

    if send_message(channel_id, message):
        reset_stats()
        logger.info("Daily report sent successfully.")
    else:
        logger.error("Failed to send daily report.")

    logger.info("========== Daily Report Finished ==========")


if __name__ == "__main__":
    main()