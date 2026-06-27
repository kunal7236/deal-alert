"""
modules/auth.py

Authentication and authorization helpers.

Currently only validates whether a Telegram user is allowed
to execute administrative commands.
"""

from modules.config import get_config
from modules.log import logger


def is_admin(user_id: int) -> bool:
    """
    Check whether a Telegram user is an administrator.

    Parameters
    ----------
    user_id : int
        Telegram user ID.

    Returns
    -------
    bool
        True if the user is an admin.
    """

    admin_ids = get_config()["telegram"]["admin_ids"]

    is_authorized = user_id in admin_ids

    logger.info(
        "Admin authentication. user_id=%s authorized=%s",
        user_id,
        is_authorized,
    )

    return is_authorized