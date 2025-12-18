from download_data import download_data
from combine_data import combine_data
from move_files import move_files
import logging
from config_loader import Config
from pathlib import Path
# ---------------------------
# Setup logging
# ---------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# ---------------------------
# Load configuration
# ---------------------------
Config.load()
OD_DATA_URL: str = Config.OD_SOURCE_URL
RAW_DATA_DIR: Path = Config.RAW_DATA_DIR
DOWNLOAD_DATA: bool = Config.DOWNLOAD_DATA
COMBINED_DATA_DIR: Path = Config.COMBINED_DATA_DIR
OUTPUT_FILE: Path = Config.COMBINED_OUTPUT_FILE
COMBINE_DATA: bool = Config.COMBINE_DATA


# ---------------------------
# Download Data
download_data(OD_DATA_URL = OD_DATA_URL, 
              RAW_DATA_DIR = RAW_DATA_DIR,
              DOWNLOAD_DATA = DOWNLOAD_DATA)
# ---------------------------

# Combine Data
combine_data(RAW_DATA_DIR = RAW_DATA_DIR,
             COMBINE_DATA_DIR = COMBINED_DATA_DIR, 
             OUTPUT_FILE = OUTPUT_FILE,
             COMBINE_DATA = COMBINE_DATA)
# ---------------------------

# Move files
move_files(RAW_DATA_DIR = RAW_DATA_DIR,
           COMBINED_DATA_DIR = COMBINED_DATA_DIR)
# ---------------------------

