from pathlib import Path
import yaml

CONFIG_PATH = Path("config/config.yaml")

class Config:
    """Centralized config loader with derived paths."""
    _config = None

    # Derived attributes
    OD_SOURCE_URL: str = None
    RAW_DATA_DIR: Path = None
    COMBINED_DATA_DIR: Path = None
    COMBINED_OUTPUT_FILE: Path = None
    DOWNLOAD_DATA: bool = False
    COMBINE_DATA: bool = False

    @classmethod
    def load(cls) -> dict:
        if cls._config is None:
            if not CONFIG_PATH.exists():
                raise FileNotFoundError(f"Config file not found: {CONFIG_PATH}")
            with CONFIG_PATH.open("r") as f:
                cls._config = yaml.safe_load(f)

            # Setup derived paths
            cls.OD_SOURCE_URL = cls._config["download_data"]["od_source_url"]
            cls.RAW_DATA_DIR = Path(cls._config["download_data"]["raw_data_dir"])
            cls.COMBINED_DATA_DIR = Path(cls._config["combined_data"]["combined_data_dir"])
            cls.COMBINED_OUTPUT_FILE = cls.COMBINED_DATA_DIR / "combined_data.csv"
            cls.DOWNLOAD_DATA = cls._config["download_data"].get("download_data_flag", False)
            cls.COMBINE_DATA = cls._config["combined_data"].get("combine_data_flag", False)
            # Adjust COMBINE_DATA based on DOWNLOAD_DATA
            if cls.DOWNLOAD_DATA:
                cls.COMBINE_DATA = True
        return cls._config

    @classmethod
    def get(cls, *keys, default=None):
        """Access nested config values via keys: get('download_data', 'raw_data_dir')"""
        cfg = cls.load()
        for key in keys:
            cfg = cfg.get(key, default)
            if cfg is default:
                break
        return cfg
