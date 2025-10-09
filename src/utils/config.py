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
SQL_DIR = PROJECT_ROOT / "sql"
SQL_SETUP_DIR = SQL_DIR / "setup"
SQL_VALIDATION_DIR = SQL_DIR / "validation"

# Data collection parameters
CURRENT_SEASON_YEARS = [2020, 2021, 2022, 2023, 2024]

# Kaggle data source configuration
KAGGLE_DATASET_ID = "sujaykapadnis/nfl-stadium-attendance-dataset"
KAGGLE_FILES = [
    {"name": "attendance", "filename": "attendance.csv"},
    {"name": "games", "filename": "games.csv"},
    {"name": "standings", "filename": "standings.csv"}
]

# ESPN API endpoints
ESPN_BASE_URL = "https://site.api.espn.com/apis/site/v2/sports/football/nfl"
ESPN_TEAMS_URL = f"{ESPN_BASE_URL}/teams"
ESPN_SCOREBOARD_URL = f"{ESPN_BASE_URL}/scoreboard"

# ESPN data source configuration
ESPN_FILES = {
    "teams": {
        "filename": "espn_teams.json",
        "path": RAW_DATA_PATH,
        "table_name": "espn_teams",
        "schema": "ESPN_TEAMS_SCHEMA"
    },
    "games": {
        "filename": "espn_games.json",
        "path": RAW_DATA_PATH,
        "table_name": "espn_games",
        "schema": "ESPN_GAMES_SCHEMA"
    }
}

# ESPN data flattening schemas
ESPN_TEAMS_SCHEMA = [
    ('id', ['team', 'id'], None),
    ('abbreviation', ['team', 'abbreviation'], ''),
    ('displayName', ['team', 'displayName'], ''),
    ('shortDisplayName', ['team', 'shortDisplayName'], ''),
    ('location', ['team', 'location'], ''),
    ('name', ['team', 'name'], ''),
    ('logo', ['team', 'logo'], '')
]

ESPN_GAMES_SCHEMA = [
    ('id', ['id'], ''),
    ('date', ['date'], ''),
    ('name', ['name'], ''),
    ('shortName', ['shortName'], ''),
    ('season', ['season', 'year'], ''),
    ('week', ['week', 'number'], ''),
    ('attendance', ['competitions', 0, 'attendance'], 0),
    ('venue_name', ['competitions', 0, 'venue', 'fullName'], ''),
    ('venue_city', ['competitions', 0, 'venue', 'address', 'city'], '')
]

# Team reference data configuration
TEAM_REFERENCE_FILES = {
    "seed": {
        "filename": "team_reference_seed.csv",
        "path": SAMPLE_DATA_PATH
    },
    "output": {
        "filename": "team_reference.csv",
        "path": RAW_DATA_PATH,
        "table_name": "team_reference"
    }
}

# SQLite database configuration
DB_NAME = "nfl_attendance.db"
DB_PATH = PROCESSED_DATA_PATH / DB_NAME

# SQL configuration
VIEW_FILES = [
    'v_teams_unified.sql',
    'v_attendance_historical.sql',
    'v_attendance_current.sql'
]

# Database validation configuration
DB_TABLES = [
    'kaggle_attendance',
    'kaggle_games', 
    'kaggle_standings',
    'espn_teams',
    'espn_games',
    'team_reference'
]

# SQL validation query
VALIDATION_QUERIES = [
    'unmapped_teams.sql'
]