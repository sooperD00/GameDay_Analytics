# GameDay Analytics - dbt Layer

## Purpose
Demonstrate dbt proficiency by answering: **"What drives NFL attendance?"**

## Structure
- **Sources:** Raw tables the Python ETL loads (`models/staging/_sources.yml`)
- **Seeds:** `team_reference_seed.csv` (team identity by season, for relocations and rebrands) and `regular_season_sizes.csv` (games per ESPN season, shared with the ESPN download)
- **Staging:** Clean raw sources (Kaggle CSVs, ESPN JSON). Four more ESPN models are parked in `models/staging/_future/`.
- **Intermediate:** Business logic (joins, calculations, time-series), including the as-of join to the team reference
- **Marts:** Analysis-ready tables (one per analytical question)
- **Tests:** Keys and not-null checks in the YAML files; completeness, cross-source, and seed-coverage checks in `tests/`; a `value_between` range test in `tests/generic/`

## Run Instructions
```bash
# From dbt_project folder (run_pipeline.sh does this for you)
dbt debug          # Test connection
dbt build          # Seeds, models, and tests in dependency order; a failed test skips what's built on it
dbt docs generate  # Create documentation (lineage starts at the raw sources)
dbt docs serve     # View in browser
```

## Analytical Questions
1. Does winning drive attendance? (home games, 2000-2019)
2. Do playoff teams get attendance boost next season? (2000-2019)
3. Does venue type (indoor/outdoor) affect attendance patterns? (regular season, 2021-2024)

## Data Sources
- **Kaggle:** Historical NFL data (2000-2019)
- **ESPN API:** Regular seasons 2020-2024 (the venue question starts at 2021, after the COVID season)
