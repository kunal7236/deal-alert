"""
modules/log.py

Central logger configuration.
"""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler

from modules.constants import LOG_DIR

LOG_DIR.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("deal-alert")

logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)

handler = RotatingFileHandler(
    LOG_DIR / "dealalert.log",
    maxBytes=10 * 1024 * 1024,   # 10 MB
    backupCount=5,
    encoding="utf-8",
)

handler.setFormatter(formatter)

logger.addHandler(handler)

# Prevent duplicate logs if imported multiple times
logger.propagate = False