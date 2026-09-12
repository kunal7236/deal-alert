"""
modules/cron.py

Cron job management.

Responsibilities:
- Read current user's crontab
- Update Deal Alert monitor schedule
- Ensure daily report job exists
"""

from __future__ import annotations

import subprocess

from modules.log import logger
from modules.constants import PROJECT_ROOT

MONITOR_TAG = "# DEAL_ALERT_MONITOR"
REPORT_TAG = "# DEAL_ALERT_REPORT"

CRONTAB_BIN = "/usr/bin/crontab"

PYTHON_BIN = PROJECT_ROOT / "venv/bin/python"

MONITOR_SCRIPT = PROJECT_ROOT / "monitor.py"
REPORT_SCRIPT = PROJECT_ROOT / "report.py"


# ---------------------------------------------------------------------
# Private Helpers
# ---------------------------------------------------------------------


def _run(command: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
    )


def _read_crontab() -> list[str]:
    """
    Read current user's crontab.
    """

    result = _run([CRONTAB_BIN, "-l"])

    if result.returncode != 0:
        logger.info("No existing crontab found.")
        return []

    return result.stdout.splitlines()


def _write_crontab(lines: list[str]) -> None:
    """
    Replace current crontab.
    """

    content = "\n".join(lines) + "\n"

    process = subprocess.run(
        [CRONTAB_BIN, "-"],
        input=content,
        text=True,
        capture_output=True,
    )

    if process.returncode != 0:
        raise RuntimeError(
            f"Unable to update crontab.\n{process.stderr}"
        )


def _replace_job(
    lines: list[str],
    tag: str,
    new_job: str,
) -> list[str]:
    """
    Replace cron entry identified by tag.

    If tag doesn't exist, append new entry.
    """

    updated = False

    for index, line in enumerate(lines):

        if tag in line:
            lines[index] = new_job
            updated = True
            break

    if not updated:
        lines.append(new_job)

    return lines


def _build_monitor_entry(minutes: int) -> str:
    return (
        f"*/{minutes} * * * * "
        f"cd {PROJECT_ROOT} && "
        f"{PYTHON_BIN} monitor.py "
        f">> {PROJECT_ROOT}/logs/cron.log 2>&1 "
        f"{MONITOR_TAG}"
    )


def _build_report_entry() -> str:
    return (
        f"0 14 * * * "
        f"cd {PROJECT_ROOT} && "
        f"{PYTHON_BIN} report.py "
        f">> {PROJECT_ROOT}/logs/cron.log 2>&1 "
        f"{REPORT_TAG}"
    )


# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------


def update_monitor_frequency(minutes: int) -> None:
    """
    Update Deal Alert monitor cron frequency.
    """

    if minutes < 1:
        raise ValueError("Frequency must be at least 1 minute.")

    lines = _read_crontab()

    lines = _replace_job(
        lines,
        MONITOR_TAG,
        _build_monitor_entry(minutes),
    )

    _write_crontab(lines)

    logger.info(
        "Monitor cron updated to every %s minute(s).",
        minutes,
    )


def ensure_report_job() -> None:
    """
    Ensure daily report cron job exists.
    """

    lines = _read_crontab()

    lines = _replace_job(
        lines,
        REPORT_TAG,
        _build_report_entry(),
    )

    _write_crontab(lines)

    logger.info("Daily report cron ensured.")
