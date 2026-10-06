import pandas as pd
import numpy as np
from src.config import CleaningConfig
from src.logger import setup_logger

logger = setup_logger("DataCleaner")

class DataCleaner:
    """Transforms raw DataFrames: type conversion, missing values, deduplication."""

    def __init__(self, config: CleaningConfig):
        self.config = config

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        logger.info(f"Raw dataset shape: {df.shape}")

        df = self._remove_duplicates(df)
        df = self._convert_types(df)
        df = self._handle_missing_values(df)

        logger.info(f"Cleaned dataset shape: {df.shape}")
        return df

    def _remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.config.drop_duplicates:
            before = len(df)
            df = df.drop_duplicates()
            logger.info(f"Removed {before - len(df)} duplicate records.")
        return df

    def _convert_types(self, df: pd.DataFrame) -> pd.DataFrame:
        for column, dtype in self.config.type_conversions.items():
            if column not in df.columns:
                logger.warning(f"Column '{column}' specified for conversion not found in DataFrame.")
                continue

            try:
                if dtype in ["integer", "int"]:
                    df[column] = pd.to_numeric(df[column], errors="coerce").astype("Int64")
                elif dtype in ["float", "numeric"]:
                    df[column] = pd.to_numeric(df[column], errors="coerce")
                elif dtype == "datetime":
                    df[column] = pd.to_datetime(df[column], errors="coerce")
                elif dtype in ["boolean", "bool"]:
                    df[column] = df[column].astype(str).str.lower().map({
                        "true": True, "1": True, "yes": True,
                        "false": False, "0": False, "no": False
                    })
                elif dtype == "string":
                    df[column] = df[column].astype(str)
            except Exception as e:
                logger.error(f"Failed converting column '{column}' to {dtype}: {e}")
        return df

    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        for column, strategy in self.config.missing_value_strategies.items():
            if column not in df.columns or not isinstance(strategy, str):
                continue

            missing_count = df[column].isnull().sum()
            if missing_count == 0:
                continue

            logger.info(f"Column '{column}' has {missing_count} missing value(s). Strategy: '{strategy}'")

            if strategy == "drop":
                df = df.dropna(subset=[column])
            elif strategy == "mean" and pd.api.types.is_numeric_dtype(df[column]):
                df[column] = df[column].fillna(df[column].mean())
            elif strategy == "median" and pd.api.types.is_numeric_dtype(df[column]):
                df[column] = df[column].fillna(df[column].median())
            elif strategy == "mode":
                mode_val = df[column].mode()
                if not mode_val.empty:
                    df[column] = df[column].fillna(mode_val[0])
            elif strategy == "fill_value":
                fill_val = self.config.fill_values.get(column)
                if fill_val is None:
                    fill_val = self.config.fill_string_values.get(column)

                if fill_val is not None:
                    df[column] = df[column].fillna(fill_val)
                else:
                    logger.warning(f"No explicit fill value defined for '{column}'. Skipping fill.")

        return df