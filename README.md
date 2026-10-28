# GameDay Analytics — Multi-Source Data Platform

> Simulates leading a data engineering initiative from discovery through production: stakeholder-driven requirements, multi-source ETL integration, collaborative schema design, and analytical validation.

**[▶ Live Dashboard](https://gamedayanalytics-ea79mgqrjngxp4xkkgdpwe.streamlit.app/)** · [View on GitHub](https://github.com/sooperD00/GameDay_Analytics)

**Core Challenge:** Integrate historical (Kaggle 2000-2019) and current (ESPN API 2020-2024) NFL data with mismatched schemas, team relocations, and inconsistent naming—then build analysis-ready models for business questions.

**Technical Approach:**
- Multi-source ETL pipeline with data quality controls
- Automated JSON schema flattening and semantic categorization (339 ESPN fields → 98 approved in review → 62 loaded so far across 7 themed tables)
- dbt transformation layer (13 models, 42 data quality tests, including completeness and cross-source checks)
- Iterative design workflow simulating cross-functional collaboration (see `/notebooks/` for analyst-engineer handoff process)

**Skills Demonstrated:**
- Python ETL (Kaggle API, ESPN REST API, CSV reference tables)
- Data modeling (dimensional design, a slowly-changing team dimension for relocations, as-of joined by season)
- SQL transformation logic (window functions, CTEs, aggregations)
- Analytical validation (correlation analysis, cohort comparisons, variability metrics)
- Technical documentation (dbt yml specs, notebook narratives, README architecture docs)

---

## 📊 Project Architecture

```
Kaggle CSV (2000-2019)  ─┐
ESPN API (2020-2024)     ├─→ Python ETL ─→ SQLite Raw Tables ─→ dbt Models ─→ Analysis Marts ─→ Streamlit
Team Reference CSV      ─┘                    (12 tables)        (13 models)     (3 marts)        dashboard
```

![Dashboard Preview](docs/dashboard_preview.png)

**Key Design Decisions:**

1. **SQLite for MVP** (not Postgres): Entire dataset <2MB, enables local development without Docker overhead. Production would use Postgres+PostGIS for geospatial queries.

2. **dbt for transformations** (not Python): Declarative SQL models with built-in testing, version control for analytics logic, easier for non-engineers to review.

3. **Themed staging tables**: Flattened ESPN's nested JSON into 7 semantic schemas (core, publicity, stats, venue, time, team_attributes, score_wins) to support varied analytical questions without creating one massive denormalized table.

4. **Curated reference table**: Manually maintained CSV for team relocations/rebrands—pragmatic choice for small, slowly-changing dataset. Each row covers a range of seasons, and models join the row active that season (an as-of join), so the Rams keep one history from St. Louis to Los Angeles. dbt tests check that every Kaggle and ESPN team maps to a row and that each franchise-season is covered exactly once.

---

## 🔍 Iterative Design Process (Technical Highlight)

**Problem:** ESPN API returns 339 nested JSON fields per game. How do you decide which to keep?

**Solution:** Simulated analyst-engineer collaboration workflow:

1. **Automated schema discovery** `/notebooks/02_view_design.ipynb`
   - Recursive JSON flattening preserving ESPN's field ordering
   - Keyword-based theme suggestion (publicity, stats, venue, etc.)
   - Automated exclusion of redundant fields (UIDs, display values, link metadata)


2. **Human review layer**: Generated CSV with sample data for "analyst" to annotate (include/exclude, rename, validate themes)

3. **Validation queries** (also `/notebooks/02_view_design.ipynb`, in the review report):
   - Constant-value field detection (found 9 fields always same value across 1,452 games)
   - Cardinality analysis (broadcasts, geolocation, etc.)
   - Data quality checks before finalizing schema

**View on nbviewer**
   - [01_exploratory_analysis.ipynb](https://nbviewer.org/github/sooperD00/GameDay_Analytics/blob/main/notebooks/01_exploratory_analysis.ipynb)
   - [02_view_design.ipynb](https://nbviewer.org/github/sooperD00/GameDay_Analytics/blob/main/notebooks/02_view_design.ipynb)
   - [03_dbt_mart_validation.ipynb](https://nbviewer.org/github/sooperD00/GameDay_Analytics/blob/main/notebooks/03_dbt_mart_validation.ipynb)

**Result:** 98 curated columns with clear semantic grouping, ready for dbt modeling. The loader brings in 62 columns today; the rest of the approved set (player leaders, extra broadcast slots) waits for a question that needs it.

*(This process demonstrates requirements engineering, data quality thinking, and pragmatic architecture—not just "run a script.")*

---

## 📈 Sample Analytical Findings

**Q1: Does winning drive attendance?** *(home games, 638 team-seasons, 2000-2019)*
- Rebuilding teams (0-4 wins): 65,516 avg home attendance
- Average teams (8-9 wins): **69,191 avg** ← *level with the best*
- Elite teams (13+ wins): 69,228 avg
- **Insight:** Winning helps, a little. Win percentage explains about 2% of the spread in home crowds (r = 0.15); stadium size and market are the likely suspects for the rest. Next step: normalize by capacity.

**Q2: Do playoff teams get attendance boost?** *(every team-season with a prior season: 228 after a playoff year, 378 after a miss)*
- After a playoff season: +0.8% avg change in home attendance
- After a missed one: -0.1% ← *comparable!*
- **Insight:** The gap is too small to tell apart from noise (Welch t-test, p = 0.09). Attendance is driven more by stadium upgrades, star signings, and pricing than by recent playoff runs.

**Q3: Does indoor vs outdoor affect stability?** *(regular-season games, 2021-2024, venues with 5+ games)*
- Indoor: 9.4% variability (lowest to highest crowd, as a share of the average)
- Outdoor: 11.6% variability
- **Insight:** Outdoor stadiums swing a little more. 2020 is left out: COVID rules capped or emptied most stadiums that year, and those games, not weather, set nearly every venue's low point.

**Second pass (Oct 2026).** A code review re-ran these questions, and the numbers above replace the first pass in [03_dbt_mart_validation.ipynb](https://nbviewer.org/github/sooperD00/GameDay_Analytics/blob/main/notebooks/03_dbt_mart_validation.ipynb):
- Kaggle's weekly attendance counts away games too. The models now average each team's own home crowds.
- Q2 first compared only the seasons where attendance rose. It now compares every season.
- The first ESPN download mixed in preseason and postseason games and missed 153 late-season ones. It now pulls complete regular seasons a week at a time, and a dbt test checks the count.

The [live dashboard](https://gamedayanalytics-ea79mgqrjngxp4xkkgdpwe.streamlit.app/) computes the same numbers from the marts, with the statistical tests behind them.

---

## 🛠️ Tech Stack

| Component | Choice | Why |
|-----------|--------|-----|
| **ETL** | Python (pandas, requests) | API integration, CSV processing, flexible transformations |
| **Storage** | SQLite | Local dev simplicity, <2MB dataset, version control friendly |
| **Transforms** | dbt Core | SQL-based models, testing framework, Git-friendly analytics |
| **Analysis** | Jupyter + SQL | Exploratory work, validation queries, documentation |
| **Dashboard** | Streamlit + Plotly | Free hosting, reads the three marts, insight text computed from the data |
| **API** | ESPN undocumented endpoints | Free, current data, required reverse-engineering (a year-only request returns the calendar year, so the pipeline asks for one week at a time) |

---

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/sooperD00/GameDay_Analytics.git
cd GameDay_Analytics

# Create a virtual environment and install dependencies (uv: https://docs.astral.sh/uv/)
# Hello! Python 3.13 shows up twice on purpose: pinned in .python-version, which uv
# and pyenv read on their own, and spelled out below so you see it without opening a dotfile.
uv venv --python 3.13         # dbt doesn't run on Python 3.14 yet
source .venv/bin/activate     # also provides `python`, which the scripts call
uv pip install -r requirements.txt
# without uv: python3.13 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt

# Run full pipeline (no Kaggle login needed: the 2000-2019 Kaggle CSVs ship in data/raw/)
bash run_pipeline.sh
```

Or run steps individually
```bash
# ETL pipeline
python -m src.etl.ingest_nfl_dataset      # keeps the bundled Kaggle CSVs; add --refresh to re-download (needs `kaggle auth login`)
python -m src.etl.ingest_current_season   # ESPN 2020-2024 regular seasons, one week at a time
python -m src.etl.create_team_reference
python -m src.etl.load_to_database

# Run dbt transformations
cd dbt_project
dbt build   # seeds, models, and all 42 tests, in dependency order
cd ..

# Refresh the dashboard's copy of the marts
python -m src.etl.export_dashboard_db
```

Explore results (from the repo root)
```bash
sqlite3 data/processed/nfl_attendance.db
> SELECT * FROM mart_win_attendance_correlation LIMIT 5;
```

Run the dashboard locally
```bash
uv pip install -r streamlit_app/requirements.txt
streamlit run streamlit_app/app.py
```

**Or just explore the notebooks:**
- `/notebooks/01_exploratory_analysis.ipynb` — Initial EDA + data integration validation
- `/notebooks/02_view_design.ipynb` — Schema design collaboration simulation
- `/notebooks/03_dbt_mart_validation.ipynb` — First-pass analytical findings + methodology (Oct 2025)

---

## 📁 Project Structure
```
GameDay_Analytics/
├── README.md
├── run_pipeline.sh              # single-command pipeline execution
├── src/                         # Python ETL — ingestion and loading
│   ├── etl/                     # ingestion scripts, dashboard export, SQL views for notebook 01
│   └── utils/                   # config.py, logging_config.py
├── dbt_project/
│   ├── seeds/                   # team_reference_seed.csv (relocation mapping), regular_season_sizes.csv
│   ├── models/
│   │   ├── staging/             # raw → clean (7 models; 4 more parked in _future/)
│   │   ├── intermediate/        # joins + window functions (3 models)
│   │   └── marts/               # analytical tables (3 models)
│   ├── tests/                   # completeness and cross-source tests (+ a generic range test)
│   └── dbt_output.txt           # captured log of the last pipeline run
├── streamlit_app/               # dashboard + its copy of the marts
├── notebooks/                   # EDA, schema design narrative, mart validation
├── data/
│   ├── sample/                  # sample CSVs for quick exploration
│   └── raw/                     # Kaggle CSVs (committed); ESPN downloads (gitignored)
└── docs/                        # extended documentation
```

**For hiring managers evaluating technical thinking:**

1. **[`/notebooks/02_view_design.ipynb`](https://nbviewer.org/github/sooperD00/GameDay_Analytics/blob/main/notebooks/02_view_design.ipynb)** ⭐ — Shows how I designed the 7-table schema through iterative refinement
2. **[`/notebooks/03_dbt_mart_validation.ipynb`](https://nbviewer.org/github/sooperD00/GameDay_Analytics/blob/main/notebooks/03_dbt_mart_validation.ipynb)** ⭐ — Demonstrates analytical rigor + business communication (the first pass; the findings above are the second)
3. **`/dbt_project/models/`** — Full staging → intermediate → marts pipeline with 42 data quality tests
4. **`/src/etl/`** — Production-style ETL with logging, error handling, idempotency

---

## 💡 What I'd Change at Scale

- **Postgres + Airflow**: SQLite → Postgres for concurrency; Python scripts → Airflow DAGs for scheduling
- **Incremental loads**: Current ETL is full refresh; add change data capture for ESPN API
- **Data catalog**: Document lineage, add metadata layer (dbt docs covers some of this)
- **Observability**: Add monitoring for API rate limits, data freshness, pipeline failures
- **Testing pyramid**: Add distribution checks (attendance drift by season) on top of today's completeness, range, and cross-source tests

---

## 🎯 Project Philosophy

This project demonstrates senior-level technical thinking:

- **Requirements translation**: Vague business question → concrete data architecture
- **Pragmatic choices**: SQLite for MVP (not over-engineering), dbt for testability (not bespoke Python)
- **Iterative refinement**: Schema design through collaboration, not upfront perfect planning
- **Production awareness**: Logging, error handling, idempotency built-in from start
- **Scale thinking**: Clear articulation of "what changes at 10x volume"

The fictional team personas (Linda, Ronald, Walter, Florence, Grace) represent different stakeholder perspectives I had to balance—data quality rigor, analytical needs, documentation clarity, statistical validity. Real data projects require synthesizing these viewpoints into coherent architecture.

---

## 📬 Contact

- **Developer:** Nicole Rowsey
- **LinkedIn:** [linkedin.com/in/nicole-rowsey](https://linkedin.com/in/nicole-rowsey)
- **Other Projects:** [github.com/sooperD00](https://github.com/sooperD00)

Currently seeking senior IC / data platform engineering roles. Open to discussing technical architecture, data modeling, or this project's design decisions.

---

**Built with Python, dbt, and iterative thinking** | [Live Dashboard](https://gamedayanalytics-ea79mgqrjngxp4xkkgdpwe.streamlit.app/) | [Explore Notebooks](notebooks/) | [View SQL Models](dbt_project/models/)
