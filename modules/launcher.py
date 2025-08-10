# modules/launcher.py

import sys
import subprocess
import shutil
from pathlib import Path
import git # GitPython

# --- Constants and Paths ---

ROOT_PATH = Path(__file__).parent.parent
WEBUI_INSTALL_PATH = ROOT_PATH / "webui_installations"
CONFIG_SOURCE_PATH = ROOT_PATH / "References" / "sdAIgen" / "__configs__"

# This dictionary maps the user-facing WebUI names to their technical details.
WEBUI_REPOS = {
    "Forge": {
        "url": "https://github.com/lllyasviel/stable-diffusion-webui-forge.git",
        "dir_name": "stable-diffusion-webui-forge",
        "config_name": "Forge"
    },
    "A1111": {
        "url": "https://github.com/AUTOMATIC1111/stable-diffusion-webui.git",
        "dir_name": "stable-diffusion-webui",
        "config_name": "A1111"
    },
    "ComfyUI": {
        "url": "https://github.com/comfyanonymous/ComfyUI.git",
        "dir_name": "ComfyUI",
        "config_name": "ComfyUI"
    }
}

# --- Helper Functions ---

class CloneProgress(git.remote.RemoteProgress):
    """A simple progress bar for the GitPython clone operation."""
    def update(self, op_code, cur_count, max_count=None, message=''):
        if max_count:
            percentage = cur_count / max_count * 100
            # Use a carriage return to keep the progress on a single line
            print(f"   Cloning... {percentage:.1f}% ({message})", end='\r')
        else:
            print(f"   Cloning... {message}", end='\r')

def _clone_repo(repo_url: str, destination_path: Path) -> bool:
    """Clones a repository to a given path with progress indication."""
    print(f"Cloning repository from {repo_url} into {destination_path}...")
    try:
        git.Repo.clone_from(repo_url, destination_path, progress=CloneProgress())
        print("\n✅ Repository cloned successfully.")
        return True
    except git.exc.GitCommandError as e:
        print(f"\n❌ Error cloning repository: {e}")
        return False

def _copy_configs(webui_name: str, webui_dest_path: Path):
    """Copies the pre-made configs from the reference repo into the WebUI directory."""
    source_config_dir = CONFIG_SOURCE_PATH / webui_name
    if not source_config_dir.is_dir():
        print(f"Note: No pre-made configs found for '{webui_name}'. Skipping configuration copy.")
        return

    print(f"Copying configuration files for '{webui_name}'...")
    # Use shutil.copytree to recursively copy files, overwriting if they exist.
    shutil.copytree(source_config_dir, webui_dest_path, dirs_exist_ok=True)
    print("✅ Configuration files copied.")

# --- Main Launch Function ---

def launch_webui(webui_config: dict):
    """
    The main function to install (if necessary) and launch the selected WebUI.
    """
    webui_name = webui_config.get("current", "Forge")
    args = webui_config.get("arguments", "").split()

    repo_info = WEBUI_REPOS.get(webui_name)
    if not repo_info:
        print(f"❌ Error: Invalid WebUI selection '{webui_name}'.")
        return

    destination_path = WEBUI_INSTALL_PATH / repo_info["dir_name"]
    config_folder_name = repo_info["config_name"]

    # --- 1. Installation Step ---
    print(f"--- Preparing WebUI: {webui_name} ---")
    if not destination_path.is_dir():
        WEBUI_INSTALL_PATH.mkdir(exist_ok=True)
        if not _clone_repo(repo_info["url"], destination_path):
            return  # Stop if cloning fails
    else:
        print(f"✅ Found existing installation at '{destination_path}'.")

    # --- 2. Configuration Step ---
    _copy_configs(config_folder_name, destination_path)

    # --- 3. Launch Step ---
    launch_script_path = destination_path / "launch.py"
    if not launch_script_path.exists():
        print(f"❌ Error: launch.py not found in '{destination_path}'")
        print("   The repository might have a different startup script or might be incomplete.")
        return

    command = [sys.executable, str(launch_script_path)] + args

    print("\n" + "="*50)
    print(f"🚀 Launching {webui_name}...")
    print(f"   ▶️  Command: {' '.join(command)}")
    print("="*50 + "\n")

    try:
        # Use Popen to start the process and stream output in real-time
        process = subprocess.Popen(
            command,
            cwd=destination_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='replace' # Avoid crashing on weird characters
        )

        # Read and print output line by line
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            if line:
                print(line, end='')
                # Highlight the public URL when it appears
                if "Running on public URL" in line:
                    print("\n" + "*"*20 + " PUBLIC URL DETECTED! " + "*"*20)

        # Wait for the process to complete and get the exit code
        return_code = process.wait()
        print(f"\n--- WebUI process exited with code: {return_code} ---")

    except FileNotFoundError:
        print(f"❌ Error: Could not find '{sys.executable}'. Is Python installed and in the PATH?")
    except Exception as e:
        print(f"\n❌ An error occurred while launching the WebUI: {e}")
