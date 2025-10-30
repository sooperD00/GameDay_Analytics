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
    "games_core": {
        "filename": "espn_games.json",
        "path": RAW_DATA_PATH,
        "table_name": "espn_games_core",
        "schema": "ESPN_GAMES_CORE_SCHEMA"
    },
    "games_publicity": {
        "filename": "espn_games.json",
        "path": RAW_DATA_PATH,
        "table_name": "espn_games_publicity",
        "schema": "ESPN_GAMES_PUBLICITY_SCHEMA"
    },
    "games_score_wins": {
        "filename": "espn_games.json",
        "path": RAW_DATA_PATH,
        "table_name": "espn_games_score_wins",
        "schema": "ESPN_GAMES_SCORE_WINS_SCHEMA"
    },
    "games_stats_data": {
        "filename": "espn_games.json",
        "path": RAW_DATA_PATH,
        "table_name": "espn_games_stats_data",
        "schema": "ESPN_GAMES_STATS_DATA_SCHEMA"
    },
    "games_team_attributes": {
        "filename": "espn_games.json",
        "path": RAW_DATA_PATH,
        "table_name": "espn_games_team_attributes",
        "schema": "ESPN_GAMES_TEAM_ATTRIBUTES_SCHEMA"
    },
    "games_time": {
        "filename": "espn_games.json",
        "path": RAW_DATA_PATH,
        "table_name": "espn_games_time",
        "schema": "ESPN_GAMES_TIME_SCHEMA"
    },
    "games_venue": {
        "filename": "espn_games.json",
        "path": RAW_DATA_PATH,
        "table_name": "espn_games_venue",
        "schema": "ESPN_GAMES_VENUE_SCHEMA"
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

# ESPN data flattening schemas - organized by analytical theme
ESPN_GAMES_CORE_SCHEMA = [
    ('id', ['id'], ''),
    ('attendance', ['competitions', 0, 'attendance'], 0),
    ('type_abbreviation', ['competitions', 0, 'type', 'abbreviation'], ''),
    ('neutralSite', ['competitions', 0, 'neutralSite'], 0),
    ('team_isActive_home', ['competitions', 0, 'competitors', 0, 'team', 'isActive'], 0),
    ('team_isActive_away', ['competitions', 0, 'competitors', 1, 'team', 'isActive'], 0),
    ('format_regulation_periods', ['competitions', 0, 'format', 'regulation', 'periods'], 0),
]

ESPN_GAMES_PUBLICITY_SCHEMA = [
    ('id', ['id'], ''),
    ('notes_headline', ['competitions', 0, 'notes', 0, 'headline'], ''),
    ('broadcasts_market_market1', ['competitions', 0, 'broadcasts', 0, 'market'], ''),
    ('broadcasts_names_market1_network1', ['competitions', 0, 'broadcasts', 0, 'names', 0], ''),
    ('broadcasts_names_market1_network2', ['competitions', 0, 'broadcasts', 0, 'names', 1], ''),
    ('broadcast', ['competitions', 0, 'broadcast'], ''),
    ('geoBroadcasts_type_shortName_broadcast1', ['competitions', 0, 'geoBroadcasts', 0, 'type', 'shortName'], ''),
    ('geoBroadcasts_market_type_broadcast1', ['competitions', 0, 'geoBroadcasts', 0, 'market', 'type'], ''),
    ('geoBroadcasts_lang_broadcast1', ['competitions', 0, 'geoBroadcasts', 0, 'lang'], ''),
    ('headlines_description', ['competitions', 0, 'headlines', 0, 'description'], ''),
    ('headlines_shortLinkText', ['competitions', 0, 'headlines', 0, 'shortLinkText'], ''),
]

ESPN_GAMES_SCORE_WINS_SCHEMA = [
    ('id', ['id'], ''),
    ('winner_home', ['competitions', 0, 'competitors', 0, 'winner'], 0),
    ('score_home', ['competitions', 0, 'competitors', 0, 'score'], ''),
    ('winner_away', ['competitions', 0, 'competitors', 1, 'winner'], 0),
    ('score_away', ['competitions', 0, 'competitors', 1, 'score'], ''),
]

ESPN_GAMES_STATS_DATA_SCHEMA = [
    ('id', ['id'], ''),
    ('playByPlayAvailable', ['competitions', 0, 'playByPlayAvailable'], 0),
    ('linescores_value_P1_home', ['competitions', 0, 'competitors', 0, 'linescores', 0, 'value'], 0),
    ('linescores_value_P2_home', ['competitions', 0, 'competitors', 0, 'linescores', 1, 'value'], 0),
    ('linescores_value_P3_home', ['competitions', 0, 'competitors', 0, 'linescores', 2, 'value'], 0),
    ('linescores_value_P4_home', ['competitions', 0, 'competitors', 0, 'linescores', 3, 'value'], 0),
    ('linescores_value_P5_home', ['competitions', 0, 'competitors', 0, 'linescores', 4, 'value'], 0),
    ('linescores_value_P1_away', ['competitions', 0, 'competitors', 1, 'linescores', 0, 'value'], 0),
    ('linescores_value_P2_away', ['competitions', 0, 'competitors', 1, 'linescores', 1, 'value'], 0),
    ('linescores_value_P3_away', ['competitions', 0, 'competitors', 1, 'linescores', 2, 'value'], 0),
    ('linescores_value_P4_away', ['competitions', 0, 'competitors', 1, 'linescores', 3, 'value'], 0),
    ('linescores_value_P5_away', ['competitions', 0, 'competitors', 1, 'linescores', 4, 'value'], 0),
]

ESPN_GAMES_TEAM_ATTRIBUTES_SCHEMA = [
    ('id', ['id'], ''),
    ('name', ['name'], ''),
    ('shortName', ['shortName'], ''),
    ('id_home', ['competitions', 0, 'competitors', 0, 'id'], ''),
    ('team_location_home', ['competitions', 0, 'competitors', 0, 'team', 'location'], ''),
    ('team_name_home', ['competitions', 0, 'competitors', 0, 'team', 'name'], ''),
    ('team_abbreviation_home', ['competitions', 0, 'competitors', 0, 'team', 'abbreviation'], ''),
    ('team_displayName_home', ['competitions', 0, 'competitors', 0, 'team', 'displayName'], ''),
    ('team_color_home', ['competitions', 0, 'competitors', 0, 'team', 'color'], ''),
    ('team_logo_home', ['competitions', 0, 'competitors', 0, 'team', 'logo'], ''),
    ('id_away', ['competitions', 0, 'competitors', 1, 'id'], ''),
    ('team_location_away', ['competitions', 0, 'competitors', 1, 'team', 'location'], ''),
    ('team_name_away', ['competitions', 0, 'competitors', 1, 'team', 'name'], ''),
    ('team_abbreviation_away', ['competitions', 0, 'competitors', 1, 'team', 'abbreviation'], ''),
    ('team_displayName_away', ['competitions', 0, 'competitors', 1, 'team', 'displayName'], ''),
    ('team_color_away', ['competitions', 0, 'competitors', 1, 'team', 'color'], ''),
    ('team_logo_away', ['competitions', 0, 'competitors', 1, 'team', 'logo'], ''),
]

ESPN_GAMES_TIME_SCHEMA = [
    ('id', ['id'], ''),
    ('season_year', ['season', 'year'], 0),
    ('season_type', ['season', 'type'], 0),
    ('season_slug', ['season', 'slug'], ''),
    ('week_number', ['week', 'number'], 0),
    ('date', ['date'], ''),
    ('startDate', ['competitions', 0, 'startDate'], ''),
]

ESPN_GAMES_VENUE_SCHEMA = [
    ('id', ['id'], ''),
    ('venue_id', ['competitions', 0, 'venue', 'id'], ''),
    ('venue_fullName', ['competitions', 0, 'venue', 'fullName'], ''),
    ('venue_address_city', ['competitions', 0, 'venue', 'address', 'city'], ''),
    ('venue_address_state', ['competitions', 0, 'venue', 'address', 'state'], ''),
    ('venue_indoor', ['competitions', 0, 'venue', 'indoor'], 0),
    ('team_venue_id_home', ['competitions', 0, 'competitors', 0, 'team', 'venue', 'id'], ''),
    ('team_venue_id_away', ['competitions', 0, 'competitors', 1, 'team', 'venue', 'id'], ''),
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