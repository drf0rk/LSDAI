# scripts/start_launcher.py
# This script orchestrates the WebUI launch process.

import sys
from pathlib import Path

# Ensure the project root is in the Python path for module importing
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from modules import config_manager
from modules import launcher

def main():
    """
    Main function to run the launch process.
    """
    print("===================================")
    print("🚀 Initializing WebUI Launch Sequence")
    print("===================================")

    # 1. Load the saved WebUI settings
    print("\n[1/2] Loading WebUI configuration...")
    webui_config = config_manager.get_setting('WEBUI')
    if not webui_config:
        print("   Error: WebUI configuration not found in settings.json.")
        print("   Please run the widget cell and save settings first.")
        return
    print(f"   ✅ Configuration loaded for '{webui_config.get('current', 'N/A')}'.")

    # 2. Execute the launcher
    print("\n[2/2] Handing off to the launcher module...")
    launcher.launch_webui(webui_config)

if __name__ == "__main__":
    main()
