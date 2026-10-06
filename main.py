import argparse
import sys
from src.pipeline import DataPipeline
from src.logger import setup_logger

logger = setup_logger("Main")

def main():
    parser = argparse.ArgumentParser(description="Generic ETL Data Processing Pipeline")
    parser.add_argument(
        "-c", "--config", 
        default="config/pipeline_config.yaml", 
        help="Path to YAML configuration file"
    )
    args = parser.parse_args()

    try:
        pipeline = DataPipeline(config_path=args.config)
        pipeline.run()
    except Exception as e:
        logger.critical(f"Pipeline execution failed: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()