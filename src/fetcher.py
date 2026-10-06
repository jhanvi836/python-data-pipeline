import json
from pathlib import Path
import pandas as pd
import requests
from src.config import InputConfig
from src.logger import setup_logger

logger = setup_logger("DataFetcher")

class DataFetcher:
    """Handles raw data ingestion from CSV, JSON, or REST APIs."""
    
    def __init__(self, config: InputConfig):
        self.config = config

    def fetch(self) -> pd.DataFrame:
        source_type = self.config.source_type.lower()
        logger.info(f"Ingesting data from source type: {source_type}")

        if source_type == "csv":
            return self._read_csv()
        elif source_type == "json":
            return self._read_json()
        elif source_type == "api":
            return self._read_api()
        else:
            raise ValueError(f"Unsupported source type: {source_type}")

    def _read_csv(self) -> pd.DataFrame:
        if not self.config.file_path or not Path(self.config.file_path).exists():
            raise FileNotFoundError(f"CSV file not found: {self.config.file_path}")
        return pd.read_csv(self.config.file_path)

    def _read_json(self) -> pd.DataFrame:
        if not self.config.file_path or not Path(self.config.file_path).exists():
            raise FileNotFoundError(f"JSON file not found: {self.config.file_path}")
        return pd.read_json(self.config.file_path)

    def _read_api(self) -> pd.DataFrame:
        if not self.config.api_url:
            raise ValueError("API source requested but 'api_url' is not defined.")
        
        try:
            response = requests.get(self.config.api_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Extract nested list if response is a dict containing a list key
            if isinstance(data, dict):
                for val in data.values():
                    if isinstance(val, list):
                        data = val
                        break
                        
            return pd.DataFrame(data)
        except requests.RequestException as e:
            logger.error(f"Failed to fetch data from API {self.config.api_url}: {e}")
            raise