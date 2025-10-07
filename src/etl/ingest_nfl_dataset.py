"""
ETL Script: NFL Dataset Ingestion
Author: Linda B. Low-k-dielectric
Date: Week 1
Purpose: Download NFL stadium attendance dataset from Kaggle with freshness checks
"""

import logging
from datetime import datetime
from pathlib import Path
from kaggle.api.kaggle_api_extended import KaggleApi
from logging.handlers import RotatingFileHandler

DATASET_ID = "sujaykapadnis/nfl-stadium-attendance-dataset"
RAW_DATA_PATH = Path(__file__).parent.parent.parent / "data" / "raw"
LOG_PATH = Path(__file__).parent.parent.parent / "logs"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_PATH / 'etl_ingest.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)



def main():
    """Ingest NFL dataset from Kaggle with freshness checks."""
    logger.info("Starting NFL dataset ingestion")
    
    api = authenticate_kaggle()
    ensure_directory_exists()
    
    if dataset_needs_update(api):
        download_dataset(api)
        logger.info("Ingestion complete - files updated")
    else:
        logger.info("Local data is up to date - no download needed")

def authenticate_kaggle():
    """Initialize and authenticate Kaggle API."""
    logger.info("Authenticating with Kaggle API")
    api = KaggleApi()
    api.authenticate()
    return api

def ensure_directory_exists():
    """Create raw data directory if it doesn't exist."""
    RAW_DATA_PATH.mkdir(parents=True, exist_ok=True)
    LOG_PATH.mkdir(parents=True, exist_ok=True)
    logger.debug(f"Ensured directories exist: {RAW_DATA_PATH}, {LOG_PATH}")

def dataset_needs_update(api):
    """
    Compare remote and local file dates to determine if update needed.
    Note: Using _creation_date as proxy since Kaggle API doesn't expose update timestamps.
    """
    logger.info(f"Checking dataset freshness: {DATASET_ID}")
    files = api.dataset_list_files(DATASET_ID).files
    needs_update = False
    
    for f in files:
        local_file = RAW_DATA_PATH / f.name
        
        if local_file.exists():
            local_date = datetime.fromtimestamp(local_file.stat().st_mtime)
            kaggle_date = f._creation_date
            logger.info(f"{f.name}: Local={local_date.date()}, Kaggle={kaggle_date.date()}")
            
            if kaggle_date > local_date:
                needs_update = True
                logger.warning(f"{f.name}: Remote version is newer")
        else:
            logger.warning(f"{f.name}: Not found locally")
            needs_update = True
    
    return needs_update

def download_dataset(api):
    """Download dataset from Kaggle."""
    logger.info(f"Downloading {DATASET_ID}")
    api.dataset_download_files(DATASET_ID, path=str(RAW_DATA_PATH), unzip=True)
    logger.info("Download complete")

if __name__ == "__main__":
    main()