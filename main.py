from src.download_data import download_data
from src.combine_data import combine_data
from src.move_files import move_files
from src.process_data import process_data
import logging
from config.config_loader import Config
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
COMBINED_OUTPUT_FILE: Path = Config.COMBINED_OUTPUT_FILE
COMBINE_DATA: bool = Config.COMBINE_DATA
PROCESS_DATA_DIR: Path = Config.PROCESS_DATA_DIR
PROCESS_DATA_FILE: Path = Config.PROCESS_OUTPUT_FILE


# ---------------------------
# Download Data
COMBINE_DATA = download_data(OD_DATA_URL = OD_DATA_URL, 
                            RAW_DATA_DIR = RAW_DATA_DIR,
                            DOWNLOAD_DATA = DOWNLOAD_DATA,
                            COMBINE_DATA = COMBINE_DATA)
# ---------------------------

# Combine Data
combine_data(RAW_DATA_DIR = RAW_DATA_DIR,
             COMBINE_DATA_DIR = COMBINED_DATA_DIR, 
             OUTPUT_FILE = COMBINED_OUTPUT_FILE,
             COMBINE_DATA = COMBINE_DATA)
# ---------------------------

# Move files
move_files(RAW_DATA_DIR = RAW_DATA_DIR,
           COMBINED_DATA_DIR = COMBINED_DATA_DIR)
# ---------------------------

# Process Data
process_data(COMBINED_DATA_DIR = COMBINED_DATA_DIR,
             COMBINED_OUTPUT_FILE = COMBINED_OUTPUT_FILE,
             SUBURBS_PATH = Config.SUBURBS_SHAPEFILE,
             OUTPUT_DIR = PROCESS_DATA_DIR,
             OUTPUT_FILE = PROCESS_DATA_FILE
    
)
