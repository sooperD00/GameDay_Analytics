#!/bin/bash
set -e  # stop on first failure

echo "=== GameDay Analytics Pipeline ==="

echo ">> Ingesting historical data (Kaggle)"
python -m src.etl.ingest_nfl_dataset

echo ">> Ingesting current season data (ESPN)"
python -m src.etl.ingest_current_season

echo ">> Creating team reference table"
python -m src.etl.create_team_reference

echo ">> Loading to database"
python -m src.etl.load_to_database

echo ">> Running dbt transformations"
cd dbt_project
dbt seed
dbt run
dbt test

echo "=== Pipeline complete ==="