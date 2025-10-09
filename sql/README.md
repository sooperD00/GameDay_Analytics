# SQL Scripts

## Setup
Database views for integrated data model. Run automatically by `load_to_database.py`.

- **v_teams_unified.sql** - Unified team names with relocation tracking
- **v_attendance_historical.sql** - Kaggle data (2000-2019) with team mapping
- **v_attendance_current.sql** - ESPN data (2020-2024) attendance records

## Validation
Data quality checks run during database load.

- **unmapped_teams.sql** - Identifies teams in historical data without reference mapping

## Analysis
Ad-hoc queries and exploration (future work).
