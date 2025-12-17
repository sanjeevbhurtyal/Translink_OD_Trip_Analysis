import logging
from pathlib import Path
import pandas as pd
from config_loader import Config
from schema import SCHEMA_TRANSLINK_OD_TRIPS

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

RAW_DATA_DIR: Path = Config.RAW_DATA_DIR
COMBINED_DATA_DIR: Path = Config.COMBINED_DATA_DIR
COMBINED_DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE: Path = Config.COMBINED_OUTPUT_FILE
COMBINE_DATA: bool = Config.COMBINE_DATA

# Define data types
DTYPE_DICT = SCHEMA_TRANSLINK_OD_TRIPS

# ---------------------------
# Combine CSV files
# ---------------------------
def load_csv_safe(file_path: Path) -> pd.DataFrame:
    """Load CSV safely with dtype and low_memory handling."""
    try:
        df = pd.read_csv(file_path, dtype=DTYPE_DICT, low_memory=False)
        return df
    except Exception as e:
        logging.error(f"Failed to load {file_path}: {e}")
        return pd.DataFrame()

def combine_csv_files(raw_dir: Path) -> pd.DataFrame:
    """Combine only CSV files that match the expected schema into a single DataFrame."""
    
    csv_files = list(raw_dir.glob("*.csv"))
    if not csv_files:
        logging.warning(f"No CSV files found in {raw_dir}")
        return pd.DataFrame()

    logging.info(f"Found {len(csv_files)} CSV files. Checking schema and combining...")

    expected_columns = set(SCHEMA_TRANSLINK_OD_TRIPS.keys())
    df_list = []

    for csv_file in csv_files:
        df = load_csv_safe(csv_file)
        if df.empty:
            logging.info(f"Skipping empty file: {csv_file.name}")
            continue

        file_columns = set(df.columns)
        if file_columns == expected_columns:
            df_list.append(df)
        else:
            logging.warning(f"Skipping file due to schema mismatch: {csv_file.name}. "
                            f"Expected columns: {expected_columns}, Found: {file_columns}")

    if df_list:
        combined_df = pd.concat(df_list, ignore_index=True)
        logging.info(f"Combined DataFrame has {len(combined_df)} rows and {len(combined_df.columns)} columns.")
        return combined_df
    else:
        logging.warning("No valid CSV files matched the schema. Returning empty DataFrame.")
        return pd.DataFrame()

# ---------------------------
# Main
# ---------------------------
def main():
    if COMBINE_DATA is False:
        logging.info("COMBINE_DATA_FLAG is set to False. Skipping combination step.")
        return

    combined_df = combine_csv_files(RAW_DATA_DIR)
    if not combined_df.empty:
        combined_df.to_csv(OUTPUT_FILE, index=False)
        logging.info(f"Saved combined data to {OUTPUT_FILE}")
    else:
        logging.warning("No data saved. Combined DataFrame is empty.")

if __name__ == "__main__":
    main()
