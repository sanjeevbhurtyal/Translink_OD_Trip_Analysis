import logging
from pathlib import Path
from typing import List
from urllib.parse import urljoin
from datetime import datetime
import yaml
import requests
from bs4 import BeautifulSoup
from zipfile import ZipFile
import shutil

# ---------------------------
# Helper functions
# ---------------------------
def get_resource_links(url: str) -> List[str]:
    """Scrape webpage and return resource links containing '/resource/'."""
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    links = [a['href'] for a in soup.find_all('a', href=True) if '/resource/' in a['href']]
    logging.info(f"Found {len(links)} files on page.")
    return links

def get_download_link(resource_url: str) -> str:
    """Scrape resource page to find actual download link ending with .zip"""
    response = requests.get(resource_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    tag = soup.find('a', href=lambda x: x and (x.endswith('.zip') or x.endswith('.csv')))
    if tag:
        return urljoin(resource_url, tag['href'])
    return None

def download_file(url: str, target_path: Path) -> None:
    """Download a file from a URL to a target path."""
    logging.info(f"Downloading {Path(url).name}")
    response = requests.get(url)
    response.raise_for_status()
    with target_path.open("wb") as f:
        f.write(response.content)

def extract_zip(zip_path: Path, extract_dir: Path) -> None:
    """Extract a zip file and keep only CSV files."""
    with ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
        # Remove non-CSV files
        for item in zip_ref.namelist():
            item_path = extract_dir / item
            if not item.endswith('.csv') and item_path.exists():
                item_path.unlink()
    zip_path.unlink()  # Remove zip after extraction


def record_download(file_path: Path, url: str) -> None:
    """Record a downloaded resource URL."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with file_path.open("a") as f:
        f.write(f"{timestamp} | {url}\n")

# ---------------------------
# Main processing
# ---------------------------
def download_data(OD_DATA_URL: str, 
             RAW_DATA_DIR: Path,
             DOWNLOAD_DATA: bool) -> None:
    """Download data files from the OD data source."""
    resource_links = get_resource_links(OD_DATA_URL)
    if DOWNLOAD_DATA is False:
        logging.info(f"DOWNLOAD_DATA is set to False. Exiting without downloading.")
        return
    
    # Clear RAW_DATA_DIR before downloading
    if RAW_DATA_DIR.exists():
        logging.info(f"Clearing existing files in {RAW_DATA_DIR}")
        shutil.rmtree(RAW_DATA_DIR)

    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    logging.info(f"Downloading files to {RAW_DATA_DIR}")
    for link in resource_links:
        try:
            resource_url = urljoin(OD_DATA_URL, link)
            download_link = get_download_link(resource_url)
            if not download_link:
                logging.warning(f"No downloadable resource found at {resource_url}")
                continue

            file_name = Path(download_link).name
            file_path = RAW_DATA_DIR / file_name
            if not file_path.exists():
                download_file(download_link, file_path)

            if file_path.suffix == '.zip':
                extract_zip(file_path, RAW_DATA_DIR)

        except Exception as e:
            logging.error(f"Failed to process {link}: {e}")

    # Update yaml to change download_data_flag to false
    config_path = Path("config/config.yaml")
    with config_path.open("r") as f:
        config_data = yaml.safe_load(f)
    config_data['download_data']['download_data_flag'] = False
    with config_path.open("w") as f:
        yaml.safe_dump(config_data, f)

    logging.info("Updated config.yaml to set download_data_flag to false to prevent re-downloading.")
