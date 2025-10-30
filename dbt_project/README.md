# GameDay Analytics - dbt Layer

## Purpose
Demonstrate dbt proficiency by answering: **"What drives NFL attendance?"**

## Structure
- **Staging:** Clean raw sources (Kaggle CSVs, ESPN JSON)
- **Intermediate:** Business logic (joins, calculations, time-series)
- **Marts:** Analysis-ready tables (one per analytical question)

## Run Instructions
```bash
# From dbt_project folder
dbt debug          # Test connection
dbt run            # Build all models
dbt test           # Validate data quality
dbt docs generate  # Create documentation
dbt docs serve     # View in browser
```

## Analytical Questions
1. Does winning drive attendance?
2. Do playoff teams get attendance boost next season?
3. Does venue type (indoor/outdoor) affect attendance patterns?

## Data Sources
- **Kaggle:** Historical NFL data (2000-2019)
- **ESPN API:** Current data (2023-2024)
