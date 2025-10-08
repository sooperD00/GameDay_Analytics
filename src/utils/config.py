"""
Shared configuration constants for ETL pipeline
"""

from pathlib import Path

# Project paths (relative to project root)
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_ROOT = PROJECT_ROOT / "data"
RAW_DATA_PATH = DATA_ROOT / "raw"
PROCESSED_DATA_PATH = DATA_ROOT / "processed"
SAMPLE_DATA_PATH = DATA_ROOT / "sample"
LOG_PATH = PROJECT_ROOT / "logs"

# Kaggle configuration
KAGGLE_DATASET_ID = "sujaykapadnis/nfl-stadium-attendance-dataset"

# ESPN API endpoints
ESPN_BASE_URL = "https://site.api.espn.com/apis/site/v2/sports/football/nfl"
ESPN_TEAMS_URL = f"{ESPN_BASE_URL}/teams"
ESPN_SCOREBOARD_URL = f"{ESPN_BASE_URL}/scoreboard"

# Data collection parameters
CURRENT_SEASON_YEARS = [2020, 2021, 2022, 2023, 2024]