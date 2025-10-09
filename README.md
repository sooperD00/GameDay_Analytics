
# GameDay Analytics

`GameDay Analytics` is a professional-style analytics project simulating a data initiative for a sports organization. The project demonstrates **end-to-end skills** in **multi-source ETL pipelines, SQL data modeling, and interactive dashboards**, simulating the integration of historical (2000-2019) and current (2020-2024) NFL attendance data to analyze trends and support operational decisions.

**Skills:** Python ETL, API integration, data quality controls, SQL joins, stakeholder adaptability.

## Scenario & Stakeholders

**Initial scope (Week 1):** Analyze historical NFL attendance trends (2000-2019) from publicly available datasets; identify patterns in attendance and team performance to support operational planning and fan engagement strategies.

>**Scope expansion (Mid-Sprint):** VP asks: **"Can you integrate current season data** to see if recent trends match historical patterns?" **YES!** add multi-source data pipeline + team name map for relocation handling.

- **Primary Stakeholder:** [Jordan Kaplan](https://cod-esports.fandom.com/wiki/JKap), VP of Sports Analytics  
- **Data Sources:** 
  - Historical: [Kaggle NFL Dataset](https://www.kaggle.com/datasets/sujaykapadnis/nfl-stadium-attendance-dataset) (2000-2019)
  >- `NEW` Current: ESPN API (2020-2024)
  >- `NEW` Reference: Curated team mapping table
- **Use Case:** Analyze attendance trends for operational planning and fan engagement
- **Requirements:** 
  - Reusable, documented data models  
  - Automated ETL pipelines  
  - SQL-based querying for key metrics  
  - Dashboards for visualization and reporting

## Team & Roles (Simulated)

| Role | Team Member | Responsibilities |
|------|------------|----------------|
| Data Quality & Statistical Methods | [Walter A. Shewhart](https://en.wikipedia.org/wiki/Walter_A._Shewhart) | Validate data quality, define KPIs, statistical analysis |
| ETL Pipeline Development | [Linda B. Low-k-dielectric](www.linkedin.com/in/nicole-rowsey) | Ingest raw data, transform & load datasets, automate pipelines |
| Dashboarding & Visualization | [Florence Nightingale](https://en.wikipedia.org/wiki/Florence_Nightingale) | Build dashboards, visual summaries for stakeholders |
| A/B Testing & Analysis | [Ronald A. Fisher](https://en.wikipedia.org/wiki/Ronald_Fisher) | Perform experimental analysis and hypothesis testing |
| Documentation & Reporting | [Grace M. Hopper](https://en.wikipedia.org/wiki/Grace_Hopper) | Write methodology, assumptions, insights, and README |

*Note: Team members are fictional personas representing skill sets aligned with the project.*

## Timeline & Milestones

1. **Week 1:** Identify dataset, ingest raw data  
2. **Week 2:** Clean, transform, and model data  
3. **Week 3:** Build SQL queries for core metrics  
4. **Week 4:** Develop dashboards, visualize attendance trends and team performance  
5. **Week 5:** Finalize documentation, deliver actionable insights  

## Project Structure
```bash
GameDay_Analytics/
├── README.md               # Project overview, planning notes, instructions
├── requirements.txt        # Python dependencies (production)
├── requirements-dev.txt    # Future/development dependencies
├── .gitignore              # Git ignore file
├── data/                   # Dataset storage
│   ├── sample/             # Small sample data (committed)
│   │   ├── attendance.csv
│   │   ├── games.csv
│   │   └── standings.csv
│   └── raw/                # Full dataset (ignored, downloaded via ETL)
├── logs/                   # ETL execution logs (ignored)
├── notebooks/              # Jupyter notebooks for EDA
├── src/                    # Python source code
│   ├── etl/                # ETL pipeline scripts
│   │   ├── ingest_nfl_dataset.py      # Historical data (Kaggle)
│   │   ├── ingest_current_season.py   # Current season (ESPN API)
│   │   ├── create_team_reference.py   # Team mapping table
│   │   └── load_to_database.py        # Multi-source integration
│   ├── models/             # Data modeling scripts
│   └── utils/              # Helper functions
│       ├── config.py       # Centralized configuration
│       └── logging_config.py  # Shared logging setup
├── sql/                    # SQL scripts and queries
│   ├── setup/              # Database setup (views, schemas)
│   │   ├── v_teams_unified.sql
│   │   ├── v_attendance_historical.sql
│   │   └── v_attendance_current.sql
│   ├── validation/         # Data quality checks
│   │   └── unmapped_teams.sql
│   └── analysis/           # Ad-hoc queries and analysis
├── dashboards/             # Dashboard files (Power BI/Tableau)
└── docs/                   # Extended documentation
```

## Key Deliverables

1. **Fact & Dimension Tables:** Modeled for **reusable metrics and self-service analytics**  
2. **ETL Pipelines:** Automated scripts ensuring **clean, validated, and processed data**  
3. **SQL Queries for Core Metrics:** Attendance, team performance, trends over time  
4. **Interactive Dashboards:** Drill-downs by game, team, week, and stadium  
5. **Documentation:** Methodology, assumptions, insights, and reproducible instructions  

## Methodology

- **Data Cleaning & Transformation:** Python ETL scripts  
- **Metric Aggregation & KPI Modeling:** SQL queries & data models  
- **Statistical Analysis:** Identify drivers of attendance and team performance patterns  
- **Dashboarding & Reporting:** Power BI / Tableau dashboards for stakeholders  
- **Documentation:** Transparent, reproducible methodology aligned with stakeholder expectations  

## Business Impact & Portfolio Takeaways

- **Stakeholder Alignment:** Simulates iterative feedback loops with leadership, adjusting scope based on data availability  
- **Multi-Source Data Integration:** Combining historical datasets, live APIs, and curated reference tables with data quality controls 
- **Data Engineering & Analytics Skills:** ETL, SQL modeling, dashboard creation, statistical analysis  
- **Decision Support:** Provides actionable insights for operational planning and fan engagement strategy  
- **Professional Storytelling:** Demonstrates end-to-end analytics workflow, reflecting real-world enterprise scenarios  

## Implementation

### Data Sources
- `data/sample/` - Small sample datasets and reference data (committed to git)
  - Sample CSVs for quick exploration
  - **`team_reference_seed.csv`** - Team mapping table (editable in Excel)
- `data/raw/` - Full datasets (ignored) downloaded via ETL pipeline
- `data/processed/` - Integrated SQLite database (ignored)
  - **`nfl_attendance.db`** - Multi-source database with views

### Team Reference Table Maintenance
The `team_reference_seed.csv` file maps team names across data sources and handles relocations:
- **Owner:** Can be maintained by non-technical staff using Excel/Google Sheets
- **Location:** `data/sample/team_reference_seed.csv`
- **Validation:** Automated via `create_team_reference.py` to catch errors
- **Updates needed when:** Teams relocate, rebrand, or ESPN changes team IDs

### ETL Pipeline
1. **Kaggle API credentials:** Place `kaggle.json` in `~/.kaggle/`
2. **Run historical ingestion:** `python -m src.etl.ingest_nfl_dataset`
3. **Run current season ingestion:** `python -m src.etl.ingest_current_season`
4. **Create team reference table:** `python -m src.etl.create_team_reference`
5. **Load to database:** `python -m src.etl.load_to_database`

### Database Access
The integrated database includes:
- **Tables:** Historical (Kaggle), current (ESPN), and reference data
- **Views:** `v_teams_unified`, `v_attendance_historical`, `v_attendance_current`
- **Location:** `data/processed/nfl_attendance.db`

## Next Steps (Simulated Team Roadmap)

- [x] **Download historical dataset to `data/raw/`** – *Linda, Week 1*  
  (Kaggle API integration with freshness checks)
>- [x] **`NEW` Ingest current season data from ESPN API** – *Linda, Week 1*  
  (API integration, raw data collection from ESPN)
>- [x] **`NEW` Create team reference table** – *Linda, Week 1*  
  (Create mapping table with relocation tracking)

- [ ] **Initial exploratory analysis in Jupyter notebooks** – *Ronald, Week 1–2*  
  (EDA, data profiling, highlight potential metrics and anomalies)
>- [x] **`NEW` Load integrated data to database** – *Linda, Week 2*  
  (3-way SQL joins across Kaggle + ESPN + reference table)
- [ ] **Build ETL scripts to populate `data/processed/`** – *Walter, Week 2–3*  
  (Python pipeline, data quality checks, handle anomalies)

- [ ] **Develop SQL queries for core metrics** – *Linda, Week 3*  
  (Model data for analysis, historical vs. current trend comparison)
- [ ] **Prototype dashboards & document findings** – *Florence, Week 4*  
  (Tableau/Power BI dashboards, stakeholder-facing summary)
- [ ] **Finalize insights & documentation** – *Team, Week 5*  
  (Deliver README, methodology, assumptions, actionable recommendations)
