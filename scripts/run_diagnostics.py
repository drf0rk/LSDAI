# scripts/run_diagnostics.py
# This script is the entry point for running the system diagnostics from a notebook cell.

import sys
from pathlib import Path

# Ensure the project root is in the Python path for module importing
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from modules import diagnostics

def main():
    """
    Main function to execute all diagnostic checks.
    """
    diagnostics.run_all_checks()

if __name__ == "__main__":
    main()
