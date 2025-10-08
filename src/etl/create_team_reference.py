"""
ETL Script: Team Reference Table Creation
Author: Linda B. Low-k-dielectric
Date: Week 1
Purpose: Load and validate team mapping table for multi-source integration
"""

# Standard library
import json
from pathlib import Path

# Third-party
import pandas as pd

# Local
from src.utils.logging_config import setup_logger
from src.utils.config import RAW_DATA_PATH, SAMPLE_DATA_PATH

# Logger
logger = setup_logger(__name__)


def main():
    """Load team reference seed data and validate against ESPN API."""
    logger.info("Loading team reference seed data")
    
    reference_df = load_seed_data()
    validate_with_espn_data(reference_df)
    save_reference_table(reference_df)
    
    logger.info("Team reference table creation complete")


def load_seed_data():
    """Load team reference data from seed CSV."""
    seed_file = SAMPLE_DATA_PATH / "team_reference_seed.csv"
    
    if not seed_file.exists():
        logger.error(f"Seed file not found: {seed_file}")
        raise FileNotFoundError(f"Missing team reference seed: {seed_file}")
    
    df = pd.read_csv(seed_file)
    logger.info(f"Loaded {len(df)} team entries from seed data")
    logger.info(f"  Unique teams: {df['espn_team_id'].nunique()}")
    logger.info(f"  Relocations: {len(df[df.duplicated(subset=['espn_team_id'], keep=False)])} entries")
    
    return df


def validate_with_espn_data(reference_df):
    """Validate reference table against ESPN API data."""
    espn_teams_file = RAW_DATA_PATH / "espn_teams.json"
    
    if not espn_teams_file.exists():
        logger.warning("ESPN teams data not found - skipping validation")
        logger.warning("  Run: python -m src.etl.ingest_current_season first")
        return
    
    with open(espn_teams_file, 'r') as f:
        espn_data = json.load(f)
    
    # Convert to int for comparison
    espn_ids = {int(team['team']['id']) for team in espn_data}
    reference_ids = set(reference_df['espn_team_id'].unique())
    
    missing_in_reference = espn_ids - reference_ids
    missing_in_espn = reference_ids - espn_ids
    
    if missing_in_reference:
        logger.error(f"ESPN team IDs missing from reference: {missing_in_reference}")
        logger.error("  Update data/sample/team_reference_seed.csv")
    
    if missing_in_espn:
        logger.warning(f"Reference IDs not in current ESPN data: {missing_in_espn}")
        logger.warning("  (May be historical teams - this is expected)")
    
    if not missing_in_reference and not missing_in_espn:
        logger.info("Validation passed - all current ESPN teams mapped")


def save_reference_table(df):
    """Save reference table to raw data folder."""
    RAW_DATA_PATH.mkdir(parents=True, exist_ok=True)
    output_file = RAW_DATA_PATH / "team_reference.csv"
    df.to_csv(output_file, index=False)
    logger.info(f"Saved team reference table to {output_file}")


if __name__ == "__main__":
    main()