from pathlib import Path
from src.config import load_config, PipelineConfig
from src.fetcher import DataFetcher
from src.cleaner import DataCleaner
from src.logger import setup_logger

logger = setup_logger("PipelineRunner")

class DataPipeline:
    """Orchestrates Fetching, Cleaning, Transforming, and Exporting data."""

    def __init__(self, config_path: str = "config/pipeline_config.yaml"):
        self.config: PipelineConfig = load_config(config_path)
        self.fetcher = DataFetcher(self.config.input)
        self.cleaner = DataCleaner(self.config.cleaning)

    def run(self) -> None:
        logger.info(f"Starting execution for pipeline: {self.config.name}")
        
        # 1. Fetch
        raw_df = self.fetcher.fetch()
        
        # 2. Clean & Transform
        cleaned_df = self.cleaner.clean(raw_df)
        
        # 3. Export
        self._export(cleaned_df)
        logger.info("Pipeline completed successfully.")

    def _export(self, df) -> None:
        output_path = Path(self.config.output.file_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if self.config.output.format == "csv":
            df.to_csv(output_path, index=False)
        elif self.config.output.format == "json":
            df.to_json(output_path, orient="records", indent=2)

        logger.info(f"Saved processed output ({len(df)} records) to: {output_path}")