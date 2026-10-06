import logging
import sys
from pathlib import Path

def setup_logger(name: str = "ETLPipeline", log_file: str = "pipeline.log") -> logging.Logger:
    """Configures structured console and file logging."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File Handler
    log_path = Path("logs")
    log_path.mkdir(exist_ok=True)
    file_handler = logging.FileHandler(log_path / log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger