# modules/diagnostics.py

from pathlib import Path

# Define the root path of the project relative to this file's location
ROOT_PATH = Path(__file__).parent.parent

def _print_status(check_name: str, success: bool, message: str = ""):
    """Helper function to print a formatted status line."""
    status_icon = "✅" if success else "❌"
    # Pad the check name to align the status messages
    print(f"  {status_icon} {check_name:<30} {message}")

def check_directories():
    """Checks for the existence of core project directories."""
    print("\n--- Checking Core Directories ---")
    required_dirs = [
        "assets", "configs", "modules", "scripts",
        "shared_models", "webui_installations"
    ]
    all_ok = True
    for dir_name in required_dirs:
        dir_path = ROOT_PATH / dir_name
        is_dir = dir_path.is_dir()
        _print_status(f"{dir_name}/", is_dir)
        if not is_dir:
            all_ok = False
    return all_ok

def check_config_files():
    """Checks for essential configuration files."""
    print("\n--- Checking Configuration Files ---")
    config_path = ROOT_PATH / "configs"
    required_files = ["settings.json", "models_sd15.json", "models_sdxl.json"]
    all_ok = True
    for file_name in required_files:
        file_path = config_path / file_name
        is_file = file_path.is_file()
        _print_status(f"configs/{file_name}", is_file)
        if not is_file:
            all_ok = False
    return all_ok

def check_webui_installations():
    """Checks for and lists installed WebUIs."""
    print("\n--- Checking WebUI Installations ---")
    install_path = ROOT_PATH / "webui_installations"
    if not install_path.is_dir():
        _print_status("Installation Directory", False, f"'{install_path}' not found.")
        return False

    found_webuis = [d.name for d in install_path.iterdir() if d.is_dir()]
    if not found_webuis:
        _print_status("No WebUIs Found", True, "Directory is empty.")
    else:
        print("   Found the following installations:")
        for webui in found_webuis:
             _print_status(webui, True)
    return True

def run_all_checks():
    """Runs all diagnostic checks in sequence and prints a summary."""
    print("===================================")
    print("🔍 Running System Diagnostics")
    print("===================================")

    results = {
        "Directories": check_directories(),
        "Config Files": check_config_files(),
        "WebUI Installations": check_webui_installations()
    }

    print("\n--- Summary ---")
    all_passed = True
    for check_name, status in results.items():
        if not status:
            all_passed = False
        _print_status(check_name, status, "OK" if status else "Issues found")

    print("\n===================================")
    if all_passed:
        print("✅ Diagnostics Complete. All checks passed.")
    else:
        print("❌ Diagnostics Complete. Some issues were found (see details above).")
    print("===================================")
