# modules/downloader.py

import requests
from pathlib import Path
from tqdm.auto import tqdm
import re

def _get_filename(url: str, response: requests.Response, provided_filename: str = None) -> str:
    """
    Determines the best filename for the downloaded file in a specific order:
    1. A filename provided in brackets `[filename.ext]`.
    2. The filename from the 'content-disposition' HTTP header.
    3. The filename from the end of the URL path.
    """
    if provided_filename:
        return provided_filename

    if 'content-disposition' in response.headers:
        d = response.headers['content-disposition']
        # Extract filename from header, handling quotes
        fname_match = re.findall('filename="?([^"]+)"?', d)
        if fname_match:
            return fname_match[0]

    # Fallback to deriving the name from the URL path
    return Path(urlparse(url).path).name

def download_file(url: str, destination: Path, file_name: str = None) -> bool:
    """
    Downloads a single file from a URL to a destination directory, with a progress bar.
    """
    try:
        print(f"\nConnecting to: {url}")
        with requests.get(url, stream=True, allow_redirects=True, timeout=10) as r:
            r.raise_for_status()

            final_filename = _get_filename(url, r, file_name)
            if not final_filename:
                print(f"Error: Could not determine a filename for URL: {url}")
                return False

            destination_path = destination / final_filename

            # Ensure the destination directory exists
            destination.mkdir(parents=True, exist_ok=True)

            total_size = int(r.headers.get('content-length', 0))

            print(f"Downloading '{final_filename}' to '{destination}'")
            with open(destination_path, 'wb') as f, tqdm(
                desc=final_filename,
                total=total_size,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for chunk in r.iter_content(chunk_size=8192):
                    size = f.write(chunk)
                    bar.update(size)

            print(f"✅ Successfully downloaded: {destination_path}")
            return True

    except requests.exceptions.RequestException as e:
        print(f"❌ Error downloading {url}: {e}")
        return False

def download_files(jobs: list):
    """
    Processes a list of download jobs from the model_parser.

    Args:
        jobs (list): A list of job dictionaries.
                     Each dict must have 'url' and 'destination'.
                     'fileName' is optional.
    """
    if not jobs:
        print("No download jobs to process.")
        return

    print(f"--- Starting Download Session: {len(jobs)} job(s) ---")
    success_count = 0
    failure_count = 0

    for i, job in enumerate(jobs, 1):
        print(f"\n--- Job {i}/{len(jobs)} ---")
        url = job.get('url')
        dest_str = job.get('destination')
        fname = job.get('fileName')

        if not url or not dest_str:
            print(f"Skipping invalid job: {job}")
            failure_count += 1
            continue

        if download_file(url, Path(dest_str), fname):
            success_count += 1
        else:
            failure_count += 1

    print("\n--- Download Summary ---")
    print(f"✅ Successful: {success_count}")
    print(f"❌ Failed:     {failure_count}")
    print("------------------------")
