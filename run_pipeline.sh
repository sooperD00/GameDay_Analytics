#!/bin/bash
# GameDay Analytics: one command from raw data to the dashboard's database.
# Runs from any folder:  bash run_pipeline.sh
set -euo pipefail  # stop on the first failed step, including a failure inside a pipe
cd "$(dirname "$0")"

for tool in python dbt; do
    if ! command -v "$tool" >/dev/null 2>&1; then
        echo "'$tool' not found. Activate the virtual environment first: source .venv/bin/activate" >&2
        exit 1
    fi
done

echo "=== GameDay Analytics Pipeline ==="

echo ">> Ingesting historical data (Kaggle)"
python -m src.etl.ingest_nfl_dataset

echo ">> Ingesting 2020-2024 seasons (ESPN)"
python -m src.etl.ingest_current_season

echo ">> Creating team reference table"
python -m src.etl.create_team_reference

echo ">> Loading to database"
python -m src.etl.load_to_database

echo ">> Building dbt models and running tests"
# dbt build = seed + run + test in dependency order. A failed test skips every model
# built on top of it, so bad data never reaches the marts. The log doubles as the
# portfolio snapshot in dbt_project/ (no color codes, so it reads cleanly on GitHub).
(cd dbt_project && dbt build --no-use-colors) | tee dbt_project/dbt_output.txt

echo ">> Exporting marts for the dashboard"
python -m src.etl.export_dashboard_db

echo "=== Pipeline complete ==="
