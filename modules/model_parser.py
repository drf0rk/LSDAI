# modules/model_parser.py

import re
from pathlib import Path
from . import data_loader

# Define the root path for all shared models
SHARED_MODELS_PATH = Path(__file__).parent.parent / "shared_models"
WEBUI_PATH = Path(__file__).parent.parent / "webui_installations"

# This maps the tags from the "File.txt" feature to their destination directories.
# It's the core of the custom download logic.
DESTINATION_MAP = {
    # Tag: Destination Path
    "model": SHARED_MODELS_PATH / "Stable-diffusion",
    "vae": SHARED_MODELS_PATH / "VAE",
    "lora": SHARED_MODELS_PATH / "Lora",
    "embedding": SHARED_MODELS_PATH / "embeddings",
    "controlnet": SHARED_MODELS_PATH / "ControlNet",
    "upscale": SHARED_MODELS_PATH / "ESRGAN", # Example for ESRGAN upscalers
    "extension": WEBUI_PATH / "extensions", # Example for extensions
    # TODO: Add all other tags from the sdAIgen wiki (clip, etc.)
}

# This maps the user-facing tags (long and short) to our internal type names.
TAG_MAP = {
    # User Tag: Internal Type
    "#model": "model", "$ckpt": "model",
    "#vae": "vae", "$vae": "vae",
    "#lora": "lora", "$lora": "lora",
    "#embedding": "embedding", "$emb": "embedding",
    "#controlnet": "controlnet", "$cnet": "controlnet",
    "#upscale": "upscale", "$ups": "upscale",
    "#extension": "extension", "$ext": "extension",
    # TODO: Add all other tags
}

def _parse_custom_urls(text: str) -> list:
    """
    Parses the text from the 'Empowerment' text area, handling tags and custom filenames.
    This implements the stateful parsing logic from the sdAIgen wiki.
    """
    download_jobs = []
    current_type = None

    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("//"):  # Ignore empty lines and comments
            continue

        # A line can contain a tag, a URL, or both.
        # Check if the line *is* or *starts with* a known tag.
        temp_line = line
        for tag, type_name in TAG_MAP.items():
            if temp_line.lower().startswith(tag):
                current_type = type_name
                # The rest of the line after the tag might be a URL
                temp_line = temp_line[len(tag):].strip()
                break # Stop after finding the first matching tag on a line

        # If the line (or remainder of the line) is empty, move to the next line
        if not temp_line:
            continue
        
        # If we have a valid type, the rest of the line is treated as a URL
        if current_type:
            url = temp_line
            fileName = None
            
            # Check for custom filename syntax [filename.ext]
            match = re.search(r'\[(.*?)\]', url)
            if match:
                fileName = match.group(1)
                url = url.replace(f"[{fileName}]", "").strip()

            destination = DESTINATION_MAP.get(current_type)
            if destination:
                download_jobs.append({
                    'url': url,
                    'destination': str(destination),
                    'fileName': fileName  # Can be None
                })
            else:
                print(f"Warning: No destination configured for type '{current_type}'")
    
    return download_jobs

def parse_download_requests(widget_config: dict) -> list:
    """
    The main function to parse all download requests from the UI.
    It combines standard dropdown selections with custom URL text.
    
    Args:
        widget_config (dict): The 'WIDGETS' section of the settings dictionary.

    Returns:
        A list of download job dictionaries.
    """
    all_jobs = []

    # --- 1. Process Standard Dropdown Selections ---
    # This logic will be fully implemented once the data_loader is updated
    # to support returning the full file list for a given model key.
    # For now, we have the placeholder logic.

    # --- 2. Process Custom URLs / Empowerment Text ---
    custom_urls_text = widget_config.get('custom_urls', '')
    if custom_urls_text:
        custom_jobs = _parse_custom_urls(custom_urls_text)
        all_jobs.extend(custom_jobs)

    # --- 3. Remove Duplicate Jobs ---
    # This ensures that if a URL is specified in both dropdowns and custom text,
    # it's only downloaded once.
    unique_jobs = []
    seen_urls = set()
    for job in all_jobs:
        if job['url'] not in seen_urls:
            unique_jobs.append(job)
            seen_urls.add(job['url'])

    return unique_jobs
