"""
monitor.py

Deal monitoring entry point.
Executed by cron.
"""

from __future__ import annotations

import time

from modules.api import fetch_deals
from modules.log import logger
from modules.matcher import match_deal, reload_keywords
from modules.runtime import update_runtime
from modules.stats import increment_matches, increment_run
from modules.storage import load_seen, save_seen
from modules.telegram import send_message
from modules.config import get_config
from modules.exceptions import ApiError
from modules.formatter import format_deal_message

def main() -> None:

    logger.info("========== Monitor Started ==========")

    reload_keywords()

    start = time.perf_counter()

    try:

        deals = fetch_deals()

    except ApiError as exc:

        logger.exception("API request failed.")

        update_runtime(
            status="API_ERROR",
            api_response_ms=None,
            deals_received=0,
            keyword_matches=0,
            notifications_sent=0,
        )

        return

    elapsed_ms = int((time.perf_counter() - start) * 1000)

    seen = load_seen()

    current_seen = set()

    matches = 0

    notifications = 0

    channel_id = get_config()["telegram"]["channel_id"]

    for deal in deals:

        matched_keyword = match_deal(deal)

        if matched_keyword is None:
            continue

        matches += 1

        pid = deal["pid"]

        current_seen.add(pid)

        if pid in seen:
            continue

        message = format_deal_message(
            deal,
            matched_keyword,
        )

        if send_message(channel_id, message):
            notifications += 1

    save_seen(current_seen)

    increment_run()

    increment_matches(matches)

    update_runtime(
        status="SUCCESS",
        api_response_ms=elapsed_ms,
        deals_received=len(deals),
        keyword_matches=matches,
        notifications_sent=notifications,
    )

    logger.info("========== Monitor Finished ==========")


if __name__ == "__main__":
    main()