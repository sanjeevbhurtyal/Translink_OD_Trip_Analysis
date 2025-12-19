from pathlib import Path
import logging
from config.files_to_move import FILES_TO_MOVE

def move_files(RAW_DATA_DIR: Path, COMBINED_DATA_DIR: Path) -> None:
    files_to_move = FILES_TO_MOVE
    # Create the COMBINED_DATA_DIR if it doesn't exist
    COMBINED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    for src_filename, dest_filename in files_to_move.items():
        src_path = RAW_DATA_DIR / src_filename
        dest_path = COMBINED_DATA_DIR / dest_filename
        if src_path.exists():
            logging.info(f"Renaming {src_path} to {dest_path}")
            src_path.rename(dest_path)
        else:
            logging.warning(f"Source file {src_path} does not exist and cannot be renamed.")
# ---------------------------