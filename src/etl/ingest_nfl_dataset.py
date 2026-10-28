"""
ETL Script: NFL Dataset Ingestion
Author: Linda B. Low-k-dielectric
Date: Week 1
Purpose: Download NFL stadium attendance dataset from Kaggle with freshness checks

The Kaggle dataset is a fixed 2000-2019 snapshot, and its three CSVs ship with the
repo in data/raw/. When they're all there, this step keeps them and never contacts
Kaggle, so the pipeline runs without a Kaggle login. To check Kaggle for a newer
version anyway (needs `kaggle auth login`):

    python -m src.etl.ingest_nfl_dataset --refresh
"""

# Standard library
import sys
from datetime import datetime

# Local
from src.utils.logging_config import setup_logger
from src.utils.config import RAW_DATA_PATH, KAGGLE_DATASET_ID, KAGGLE_FILES

# Logger
logger = setup_logger(__name__)


def main(refresh=False):
    """Keep the bundled Kaggle CSVs, or download them when missing or asked to refresh."""
    logger.info("Starting NFL dataset ingestion")
    ensure_directory_exists()

    missing = [f["filename"] for f in KAGGLE_FILES if not (RAW_DATA_PATH / f["filename"]).exists()]
    if not missing and not refresh:
        logger.info("All Kaggle CSVs are in data/raw/ - keeping them (pass --refresh to check Kaggle)")
        return

    if missing:
        logger.warning(f"Missing from data/raw/: {', '.join(missing)}")

    api = authenticate_kaggle()
    if missing or dataset_needs_update(api):
        download_dataset(api)
        logger.info("Ingestion complete - files updated")
    else:
        logger.info("Local data is up to date - no download needed")

def authenticate_kaggle():
    """Initialize and authenticate Kaggle API."""
    # Imported here rather than at the top: importing kaggle tries to log in
    # right away, and the default path in main() never needs Kaggle.
    from kaggle.api.kaggle_api_extended import KaggleApi

    logger.info("Authenticating with Kaggle API")
    api = KaggleApi()
    api.authenticate()
    return api

def ensure_directory_exists():
    """Create raw data directory if it doesn't exist."""
    RAW_DATA_PATH.mkdir(parents=True, exist_ok=True)
    logger.debug(f"Ensured directory exists: {RAW_DATA_PATH}")

def dataset_needs_update(api):
    """
    Compare remote and local file dates to determine if update needed.
    Note: Using creation_date as proxy since Kaggle API doesn't expose update timestamps.
    """
    logger.info(f"Checking dataset freshness: {KAGGLE_DATASET_ID}")
    files = api.dataset_list_files(KAGGLE_DATASET_ID).files
    needs_update = False

    for f in files:
        local_file = RAW_DATA_PATH / f.name

        if local_file.exists():
            local_date = datetime.fromtimestamp(local_file.stat().st_mtime)
            kaggle_date = f.creation_date
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
    logger.info(f"Downloading {KAGGLE_DATASET_ID}")
    api.dataset_download_files(KAGGLE_DATASET_ID, path=str(RAW_DATA_PATH), unzip=True)
    logger.info("Download complete")

if __name__ == "__main__":
    main(refresh="--refresh" in sys.argv[1:])
