"""
modules/exceptions.py

Custom exceptions used by Deal Alert.
"""


class DealAlertError(Exception):
    """Base exception for the project."""


class ConfigError(DealAlertError):
    """Configuration related errors."""


class StorageError(DealAlertError):
    """Storage related errors."""


class ApiError(DealAlertError):
    """Deals API related errors."""


class TelegramError(DealAlertError):
    """Telegram Bot API related errors."""