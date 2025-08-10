# modules/config_manager.py

import json
from pathlib import Path

# Define the path to the settings file relative to the project root.
# Assumes this module is in `modules/` and the config is in `configs/`.
SETTINGS_FILE = Path(__file__).parent.parent / "configs" / "settings.json"

def _read_config():
    """
    Reads the entire configuration file.
    Returns an empty dictionary if the file doesn't exist or is corrupted.
    """
    if not SETTINGS_FILE.exists():
        return {}
    try:
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        print(f"Warning: Could not read or parse settings file at {SETTINGS_FILE}. Returning empty config.")
        return {}

def _write_config(config_data):
    """Writes the entire configuration data to the file."""
    try:
        # Ensure the parent directory exists
        SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(config_data, f, indent=4)
    except IOError:
        print(f"Error: Could not write to settings file at {SETTINGS_FILE}")

def get_setting(section: str, key: str, default=None):
    """
    Retrieves a specific setting from a section of the config file.

    Args:
        section (str): The section of the configuration (e.g., 'WEBUI').
        key (str): The key within the section.
        default: The value to return if the key or section is not found.

    Returns:
        The value of the setting, or the default value.
    """
    config = _read_config()
    return config.get(section, {}).get(key, default)

def get_section(section: str) -> dict:
    """
    Retrieves an entire section from the config file.

    Args:
        section (str): The section of the configuration (e.g., 'WIDGETS').

    Returns:
        A dictionary of the section, or an empty dictionary if not found.
    """
    config = _read_config()
    return config.get(section, {})

def set_setting(section: str, key: str, value):
    """
    Sets a specific setting in a section of the config file.

    Args:
        section (str): The section of the configuration (e.g., 'WEBUI').
        key (str): The key within the section.
        value: The value to set for the key.
    """
    config = _read_config()
    if section not in config:
        config[section] = {}
    config[section][key] = value
    _write_config(config)

def get_full_config():
    """Returns the entire configuration dictionary."""
    return _read_config()
