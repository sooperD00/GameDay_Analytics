"""
ETL Script: Multi-Source Database Loading
Author: Linda B. Low-k-dielectric
Date: Week 2
Purpose: Load and integrate Kaggle, ESPN, and reference data into SQLite database
"""

# Standard library
import json
import sqlite3
from pathlib import Path

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
    SQL_VALIDATION_DIR,
    VIEW_FILES,
    DB_TABLES,
    VALIDATION_QUERIES
)

# Logger
logger = setup_logger(__name__)


def main():
    """Load all data sources into integrated SQLite database."""
    logger.info("Starting multi-source database load")
    
    ensure_directories()
    conn = create_database()
    
    try:
        load_kaggle_data(conn)
        load_espn_data(conn)
        load_reference_data(conn)
        create_integrated_views(conn)
        validate_data(conn)
        
        logger.info("Database load complete")
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


def load_kaggle_data(conn):
    """Load historical Kaggle CSV files into database."""
    logger.info("Loading Kaggle historical data (2000-2019)")
    
    for file_config in KAGGLE_FILES:
        file_path = RAW_DATA_PATH / file_config["filename"]
        table_name = f"kaggle_{file_config['name']}"
        
        if not file_path.exists():
            logger.warning(f"  File not found: {file_path}")
            continue
        
        try:
            df = pd.read_csv(file_path)  # Pandas will error if not CSV
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            logger.info(f"  Loaded {len(df)} records into {table_name}")
        except Exception as e:
            logger.error(f"  Error loading {file_path}: {e}")



def load_espn_data(conn):
    """Load current ESPN JSON data into database."""
    logger.info("Loading ESPN current season data (2020-2024)")
    
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
    
    for data_type, config in ESPN_FILES.items():
        file_path = RAW_DATA_PATH / config["filename"]
        
        if not file_path.exists():
            logger.warning(f"  {data_type}: File not found: {file_path}")
            continue
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)  # Will error if not valid JSON
            
            schema = schemas[config["schema"]]
            flat_data = flatten_espn_data(data, schema)
            df = pd.DataFrame(flat_data)
            df.to_sql(config["table_name"], conn, if_exists='replace', index=False)
            logger.info(f"  Loaded {len(df)} records into {config['table_name']}")
        except Exception as e:
            logger.error(f"  Error loading {data_type} from {file_path}: {e}")


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
                value = value[key] if isinstance(value, dict) else value[key]
            result[output_key] = value if value is not None else default
        except (KeyError, IndexError, TypeError):
            result[output_key] = default
    return result


def load_reference_data(conn):
    """Load team reference mapping table."""
    logger.info("Loading team reference data")
    
    ref_config = TEAM_REFERENCE_FILES["output"]
    ref_file = ref_config["path"] / ref_config["filename"]
    
    if not ref_file.exists():
        logger.error(f"  Reference file not found: {ref_file}")
        logger.error("  Run: python -m src.etl.create_team_reference")
        return
    
    try:
        df = pd.read_csv(ref_file)
        df.to_sql(ref_config["table_name"], conn, if_exists='replace', index=False)
        logger.info(f"  Loaded {len(df)} team mapping entries")
    except Exception as e:
        logger.error(f"  Error loading reference data: {e}")


def create_integrated_views(conn):
    """Create SQL views from definition files."""
    logger.info("Creating integrated views")
    
    cursor = conn.cursor()
    for view_file in VIEW_FILES:
        file_path = SQL_SETUP_DIR / view_file
        with open(file_path, 'r') as f:
            sql = f.read()
        cursor.execute(sql)
        logger.info(f"  Created view: {view_file.replace('.sql', '')}")
    
    conn.commit()


def validate_data(conn):
    """Run validation queries on loaded data."""
    logger.info("Validating loaded data")
    
    cursor = conn.cursor()
    
    # Count records in each table
    for table in DB_TABLES:
        try:
            result = cursor.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
            logger.info(f"  {table}: {result[0]} records")
        except sqlite3.OperationalError:
            logger.warning(f"  {table}: Table not found")
    
    # Run validation queries
    for query_file in VALIDATION_QUERIES:
        file_path = SQL_VALIDATION_DIR / query_file
        if not file_path.exists():
            logger.warning(f"  Validation query not found: {query_file}")
            continue
        
        with open(file_path, 'r') as f:
            sql = f.read()
        
        try:
            result = cursor.execute(sql).fetchone()
            unmapped_count = result[0]
            
            if unmapped_count > 0:
                logger.warning(f"  Found {unmapped_count} unmapped team names in historical data")
            else:
                logger.info("  All historical teams successfully mapped")
        except Exception as e:
            logger.error(f"  Error running validation query {query_file}: {e}")


if __name__ == "__main__":
    main()