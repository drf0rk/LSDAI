# modules/data_loader.py

import json
from pathlib import Path

# Define paths relative to this file's location to ensure robustness
CONFIG_PATH = Path(__file__).parent.parent / "configs"
MODELS_SD15_FILE = CONFIG_PATH / "models_sd15.json"
MODELS_SDXL_FILE = CONFIG_PATH / "models_sdxl.json"

def _load_data_file(file_path: Path):
    """
    Loads a JSON data file and returns its content.
    Returns an empty dictionary on error.
    """
    if not file_path.exists():
        print(f"Warning: Data file not found at {file_path}")
        return {}
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Warning: Could not read or parse data file at {file_path}. Error: {e}")
        return {}

def get_model_data(version: str = "sd1.5"):
    """
    Loads the model data for the specified version ('sd1.5' or 'sdxl').
    """
    if version.lower() == "sdxl":
        return _load_data_file(MODELS_SDXL_FILE)
    return _load_data_file(MODELS_SD15_FILE)

def get_model_list(version: str = "sd1.5"):
    """
    Returns a list of model names for the specified version.
    Prepends 'none' to the list for the dropdown default.
    """
    data = get_model_data(version)
    models = list(data.get("models", {}).keys())
    return ["none"] + models

def get_vae_list(version: str = "sd1.5"):
    """
    Returns a list of VAE names for the specified version.
    Prepends 'none' to the list for the dropdown default.
    """
    data = get_model_data(version)
    vaes = list(data.get("vaes", {}).keys())
    return ["none"] + vaes

def get_lora_list(version: str = "sd1.5"):
    """
    Returns a list of LoRA names for the specified version.
    Prepends 'none' to the list for the dropdown default.
    """
    data = get_model_data(version)
    loras = list(data.get("loras", {}).keys())
    return ["none"] + loras

def get_model_url(model_name: str, model_type: str, version: str = "sd1.5"):
    """
    Gets the URL for a specific model, VAE, or LoRA by name.

    Args:
        model_name (str): The name of the item to look up.
        model_type (str): The type of item ('models', 'vaes', 'loras').
        version (str): The data set to look in ('sd1.5' or 'sdxl').

    Returns:
        The URL string, or None if not found.
    """
    if model_name == "none":
        return None

    data = get_model_data(version)
    return data.get(model_type, {}).get(model_name, {}).get("url")
