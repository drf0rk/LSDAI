# scripts/start_ui.py
# This script is the main entry point for launching the user interface.
# It is designed to be run from a Jupyter cell.

import sys
from pathlib import Path

# Add the project root directory to the Python path to ensure modules can be found.
# This makes the script runnable from any working directory.
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from modules.widget_manager import WidgetManager

def main():
    """
    Initializes the WidgetManager and displays the UI.
    """
    print("Initializing User Interface...")

    # A simple check to ensure the script is run in an environment that supports IPython.
    try:
        get_ipython()
    except NameError:
        print("Error: This UI is designed to be run in an IPython environment (like Jupyter or Google Colab).")
        print("Please run this script from within a notebook cell.")
        return

    # Create an instance of our main UI class and display it.
    ui = WidgetManager()
    ui.display()

    print("User Interface is now displayed.")

if __name__ == "__main__":
    main()
