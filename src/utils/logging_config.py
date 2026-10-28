"""
Shared logging configuration for ETL pipeline
"""

import logging

from src.utils.config import LOG_PATH

def setup_logger(name):
    """
    Configure logger for ETL scripts.

    Args:
        name (str): Name of the calling module (use __name__)

    Returns:
        logging.Logger: Configured logger instance
    """
    LOG_PATH.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Avoid duplicate handlers if logger already exists
    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # File handler
        file_handler = logging.FileHandler(LOG_PATH / 'etl_ingest.log')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
