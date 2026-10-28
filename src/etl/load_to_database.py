"""
ETL Script: Multi-Source Database Loading
Author: Linda B. Low-k-dielectric
Date: Week 2
Purpose: Load and integrate Kaggle, ESPN, and reference data into SQLite database

Reads and checks every input before writing anything, so a missing file or an empty
download stops the run and leaves the previous tables in place. Any problem exits
with a non-zero code, which stops run_pipeline.sh before dbt runs on bad data.
"""

# Standard library
import json
import sqlite3
import sys

# Third-party
import pandas as pd

# Local
from src.utils.logging_config import setup_logger
from src.utils.config import (
    RAW_DATA_PATH,
    PROCESSED_DATA_PATH,
    DB_PATH,
    KAGGLE_FILES,
    ESPN_FILES,
    ESPN_TEAMS_SCHEMA,
    TEAM_REFERENCE_FILES,
    SQL_SETUP_DIR,
    VIEW_FILES,
    DB_TABLES
)

# Logger
logger = setup_logger(__name__)


def main():
    """Load all data sources into integrated SQLite database."""
    logger.info("Starting multi-source database load")

    ensure_directories()
    conn = create_database()

    try:
        # Read and check every input first; write only once all of them are good.
        tables = {**read_kaggle_data(), **read_espn_data(), **read_reference_data()}
        write_tables(conn, tables)
        create_integrated_views(conn)
        validate_data(conn)

        logger.info("Database load complete")
    except Exception:
        logger.exception("Database load failed")
        sys.exit(1)
    finally:
        conn.close()


def ensure_directories():
    """Create necessary directories."""
    PROCESSED_DATA_PATH.mkdir(parents=True, exist_ok=True)
    logger.debug(f"Ensured directory exists: {PROCESSED_DATA_PATH}")


def create_database():
    """Create SQLite database connection."""
    if DB_PATH.exists():
        logger.info(f"Connecting to existing database: {DB_PATH}")
    else:
        logger.info(f"Creating new database: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    return conn


def require_file(file_path, how_to_make_it):
    """Raise a clear error if an input file is missing."""
    if not file_path.exists():
        raise FileNotFoundError(f"{file_path} not found. Run: {how_to_make_it}")


def check_has_rows(df, table_name):
    """Refuse to load an empty table.

    pandas drops the old table before it creates the new one, so writing an empty
    DataFrame would wipe good data and then fail.
    """
    if df.empty or len(df.columns) == 0:
        raise ValueError(f"No rows to load into {table_name}; keeping the existing table")
    return df


def read_kaggle_data():
    """Read historical Kaggle CSV files."""
    logger.info("Reading Kaggle historical data (2000-2019)")
    tables = {}

    for file_config in KAGGLE_FILES:
        file_path = RAW_DATA_PATH / file_config["filename"]
        table_name = f"kaggle_{file_config['name']}"
        require_file(file_path, "python -m src.etl.ingest_nfl_dataset")

        df = pd.read_csv(file_path)  # Pandas will error if not CSV
        tables[table_name] = check_has_rows(df, table_name)

    return tables


def read_espn_data():
    """Read and flatten ESPN JSON data (2020-2024 seasons)."""
    logger.info("Reading ESPN data (2020-2024 seasons)")

    # Import all themed schemas
    from src.utils.config import (
        ESPN_GAMES_CORE_SCHEMA,
        ESPN_GAMES_PUBLICITY_SCHEMA,
        ESPN_GAMES_SCORE_WINS_SCHEMA,
        ESPN_GAMES_STATS_DATA_SCHEMA,
        ESPN_GAMES_TEAM_ATTRIBUTES_SCHEMA,
        ESPN_GAMES_TIME_SCHEMA,
        ESPN_GAMES_VENUE_SCHEMA
    )

    schemas = {
        "ESPN_TEAMS_SCHEMA": ESPN_TEAMS_SCHEMA,
        "ESPN_GAMES_CORE_SCHEMA": ESPN_GAMES_CORE_SCHEMA,
        "ESPN_GAMES_PUBLICITY_SCHEMA": ESPN_GAMES_PUBLICITY_SCHEMA,
        "ESPN_GAMES_SCORE_WINS_SCHEMA": ESPN_GAMES_SCORE_WINS_SCHEMA,
        "ESPN_GAMES_STATS_DATA_SCHEMA": ESPN_GAMES_STATS_DATA_SCHEMA,
        "ESPN_GAMES_TEAM_ATTRIBUTES_SCHEMA": ESPN_GAMES_TEAM_ATTRIBUTES_SCHEMA,
        "ESPN_GAMES_TIME_SCHEMA": ESPN_GAMES_TIME_SCHEMA,
        "ESPN_GAMES_VENUE_SCHEMA": ESPN_GAMES_VENUE_SCHEMA
    }
    tables = {}

    for data_type, config in ESPN_FILES.items():
        file_path = RAW_DATA_PATH / config["filename"]
        require_file(file_path, "python -m src.etl.ingest_current_season")

        with open(file_path, 'r') as f:
            data = json.load(f)  # Will error if not valid JSON

        schema = schemas[config["schema"]]
        df = pd.DataFrame(flatten_espn_data(data, schema))
        tables[config["table_name"]] = check_has_rows(df, config["table_name"])

    return tables


def flatten_espn_data(data, schema):
    """Flatten nested ESPN JSON using provided schema."""
    return [flatten_with_schema(item, schema) for item in data]


def flatten_with_schema(data, schema):
    """
    Generic flattening function using schema definition.

    Args:
        data: Nested dict/list to flatten
        schema: List of tuples (output_key, path_list, default_value)

    Returns:
        Flattened dict
    """
    result = {}
    for output_key, path, default in schema:
        value = data
        try:
            for key in path:
                value = value[key]  # dict key or list index
            result[output_key] = value if value is not None else default
        except (KeyError, IndexError, TypeError):
            result[output_key] = default
    return result


def read_reference_data():
    """Read team reference mapping table."""
    logger.info("Reading team reference data")

    ref_config = TEAM_REFERENCE_FILES["output"]
    ref_file = ref_config["path"] / ref_config["filename"]
    require_file(ref_file, "python -m src.etl.create_team_reference")

    df = pd.read_csv(ref_file)
    return {ref_config["table_name"]: check_has_rows(df, ref_config["table_name"])}


def write_tables(conn, tables):
    """Replace each table with its checked DataFrame."""
    logger.info("Writing tables")
    for table_name, df in tables.items():
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        logger.info(f"  Loaded {len(df)} records into {table_name}")


def create_integrated_views(conn):
    """Create SQL views from definition files.

    Drops each view before creating it: with CREATE VIEW IF NOT EXISTS, an edited
    definition never replaced the copy already in the database.
    """
    logger.info("Creating integrated views")

    cursor = conn.cursor()
    for view_file in VIEW_FILES:
        file_path = SQL_SETUP_DIR / view_file
        view_name = file_path.stem
        with open(file_path, 'r') as f:
            sql = f.read()
        cursor.execute(f"DROP VIEW IF EXISTS {view_name}")
        cursor.execute(sql)
        logger.info(f"  Created view: {view_name}")

    conn.commit()


def validate_data(conn):
    """Check that every expected table exists and has rows; stop if any doesn't.

    Note: Referential integrity checks (e.g., team mapping coverage)
    are handled by dbt test (assert_kaggle_teams_have_reference_mapping).
    """
    logger.info("Validating loaded data")

    cursor = conn.cursor()
    problems = []

    for table in DB_TABLES:
        try:
            count = cursor.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        except sqlite3.OperationalError:
            problems.append(f"{table}: table not found")
            continue
        logger.info(f"  {table}: {count} records")
        if count == 0:
            problems.append(f"{table}: no rows")

    if problems:
        raise RuntimeError("Validation failed: " + "; ".join(problems))


if __name__ == "__main__":
    main()
