from __future__ import annotations

from modules.constants import DATA_DIR
from modules.storage import load_json, save_json

_CONFIG_FILE = DATA_DIR / "config.json"

_config: dict = {}


def get_config() -> dict:
    """
    Return cached configuration.
    """
    return _config


def reload_config() -> None:
    """
    Reload configuration from disk.
    """

    global _config

    _config = load_json(_CONFIG_FILE)


def save_config(config: dict) -> None:
    """
    Save configuration to disk and update cache.

    Parameters
    ----------
    config : dict
        New configuration.
    """

    global _config

    save_json(_CONFIG_FILE, config)

    _config = config