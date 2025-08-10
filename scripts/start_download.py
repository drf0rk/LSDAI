# scripts/start_download.py
# This script orchestrates the entire download process, from reading settings
# to parsing requests and finally downloading the files.

import sys
from pathlib import Path

# Ensure the project root is in the Python path for module importing
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from modules import config_manager
from modules import model_parser
from modules import downloader

def main():
    """
    Main function to run the download process, designed to be called from a notebook cell.
    """
    print("==============================================")
    print("🚀 Starting Model Management & Download Process")
    print("==============================================")

    # Step 1: Load the configuration saved by the widgets
    print("\n[1/3] Loading saved widget settings...")
    widget_config = config_manager.get_section('WIDGETS')
    if not widget_config:
        print("   No widget settings found. Nothing to download.")
        print("==============================================")
        return
    print("   ✅ Settings loaded successfully.")

    # Step 2: Parse the configuration to generate a list of download jobs
    print("\n[2/3] Parsing download requests...")
    download_jobs = model_parser.parse_download_requests(widget_config)
    if not download_jobs:
        print("   No download jobs found to process.")
        print("==============================================")
        return
    print(f"   ✅ Found {len(download_jobs)} unique file(s) to download.")

    # Step 3: Pass the job list to the downloader and execute
    print("\n[3/3] Executing download jobs...")
    downloader.download_files(download_jobs)

    print("\n==============================================")
    print("🎉 Download Process Finished")
    print("==============================================")

if __name__ == "__main__":
    main()
