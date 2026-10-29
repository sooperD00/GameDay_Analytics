"""
ETL Script: Dashboard Database Export
Purpose: Copy the dbt marts into streamlit_app/nfl_attendance.db, the file the
         deployed dashboard (Railway) reads. data/processed/ is gitignored, so the
         deployed app can't see the pipeline's own database; this keeps the two in step.

The export holds only the mart tables the dashboard reads: no raw tables, no views.
"""

# Standard library
import sqlite3

# Local
from src.utils.logging_config import setup_logger
from src.utils.config import DB_PATH, DASHBOARD_DB_PATH, DASHBOARD_TABLES

# Logger
logger = setup_logger(__name__)


def main():
    """Write a fresh dashboard database, then swap it in place of the old one."""
    logger.info("Exporting marts for the dashboard")

    tmp_path = DASHBOARD_DB_PATH.with_name(DASHBOARD_DB_PATH.name + ".tmp")
    tmp_path.unlink(missing_ok=True)

    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute("ATTACH DATABASE ? AS dashboard", (str(tmp_path),))
        for table in DASHBOARD_TABLES:
            conn.execute(f"CREATE TABLE dashboard.{table} AS SELECT * FROM main.{table}")
            rows = conn.execute(f"SELECT COUNT(*) FROM dashboard.{table}").fetchone()[0]
            if rows == 0:
                raise ValueError(f"{table} is empty; keeping the old dashboard database")
            logger.info(f"  {table}: {rows} rows")
        conn.commit()
        conn.execute("DETACH DATABASE dashboard")
    finally:
        conn.close()

    # Swap only after every table copied, so a failure leaves the old file in place.
    tmp_path.replace(DASHBOARD_DB_PATH)
    logger.info(f"Dashboard database written to {DASHBOARD_DB_PATH}")


if __name__ == "__main__":
    main()
