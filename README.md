
# GameDay Analytics

`GameDay Analytics` is a professional-style analytics project simulating a data initiative for a sports organization. The project demonstrates **end-to-end skills** in **data ingestion, Python ETL, SQL modeling, dashboarding, and actionable reporting**, reflecting the type of work expected in senior analytics and analytics engineering roles.

---

## Scenario & Stakeholders

> **Simulated Real-World Scenario:**  
> After an initial scoping session with the VP of Sports Analytics, we planned a project to optimize ticket sales and marketing campaigns using game, attendance, and promotional data. Upon reviewing available public datasets, we adjusted the project focus to **analyzing attendance trends and team performance**, delivering actionable insights to support **operational planning, staffing, and fan engagement strategies**.

- **Primary Stakeholder:** [Jordan Kaplan](https://cod-esports.fandom.com/wiki/JKap), VP of Sports Analytics  
- **Dataset:** [NFL Stadium Attendance Dataset](https://www.kaggle.com/datasets/sujaykapadnis/nfl-stadium-attendance-dataset) (Sujay Kapadnis, Kaggle)  
- **Use Case:** Analyze attendance trends and team performance to provide actionable recommendations for operational planning, fan engagement, and staffing decisions.  
- **Requirements:** 
  - Reusable, documented data models  
  - Automated ETL pipelines  
  - SQL-based querying for key metrics  
  - Dashboards for visualization and reporting  

---

## Team & Roles (Simulated)

| Role | Team Member | Responsibilities |
|------|------------|----------------|
| Data Quality & Statistical Methods | [Walter A. Shewhart](https://en.wikipedia.org/wiki/Walter_A._Shewhart) | Validate data quality, define KPIs, statistical analysis |
| ETL Pipeline Development | [Linda B. Low-k-dielectric](www.linkedin.com/in/nicole-rowsey) | Ingest raw data, transform & load datasets, automate pipelines |
| Dashboarding & Visualization | [Florence Nightingale](https://en.wikipedia.org/wiki/Florence_Nightingale) | Build dashboards, visual summaries for stakeholders |
| A/B Testing & Analysis | [Ronald A. Fisher](https://en.wikipedia.org/wiki/Ronald_Fisher) | Perform experimental analysis and hypothesis testing |
| Documentation & Reporting | [Grace M. Hopper](https://en.wikipedia.org/wiki/Grace_Hopper) | Write methodology, assumptions, insights, and README |

*Note: Team members are fictional personas representing skill sets aligned with the project.*

---

## Timeline & Milestones

1. **Week 1:** Identify dataset, ingest raw data  
2. **Week 2:** Clean, transform, and model data  
3. **Week 3:** Build SQL queries for core metrics  
4. **Week 4:** Develop dashboards, visualize attendance trends and team performance  
5. **Week 5:** Finalize documentation, deliver actionable insights  

---

## Project Structure

```bash
EventMetrics/
├── README.md               # Project overview, planning notes, instructions
├── requirements.txt        # Python dependencies (Current)
├── requirements-dev.txt      # Future/planned dependencies
├── .gitignore              # Git ignore file
├── data/                   # CSVs, raw data dumps, or SQL scripts for demo datasets
│   ├── sample/             # Committed to git - small subset for demos/testing
│   │   ├── attendance.csv
│   │   ├── games.csv
│   │   └── standings.csv
│   └── raw/                # NOT committed - full dataset from automated pipeline
│       ├── attendance.csv
│       ├── games.csv
│       └── standings.csv
├── logs/                   # ETL logs (not committed)
├── notebooks/              # Jupyter notebooks for exploration, prototyping, analysis
├── src/                    # Python scripts
│   ├── etl/                # ETL scripts
│   ├── models/             # Data modeling / transformation scripts
│   └── utils/              # Helper functions
├── sql/                    # SQL scripts / queries
├── dashboards/             # Placeholder for Power BI / Tableau dashboards
└── docs/                   # Optional extended documentation
```

---

## Key Deliverables

1. **Fact & Dimension Tables:** Modeled for **reusable metrics and self-service analytics**  
2. **ETL Pipelines:** Automated scripts ensuring **clean, validated, and processed data**  
3. **SQL Queries for Core Metrics:** Attendance, team performance, trends over time  
4. **Interactive Dashboards:** Drill-downs by game, team, week, and stadium  
5. **Documentation:** Methodology, assumptions, insights, and reproducible instructions  

---

## Methodology

- **Data Cleaning & Transformation:** Python ETL scripts  
- **Metric Aggregation & KPI Modeling:** SQL queries & data models  
- **Statistical Analysis:** Identify drivers of attendance and team performance patterns  
- **Dashboarding & Reporting:** Power BI / Tableau dashboards for stakeholders  
- **Documentation:** Transparent, reproducible methodology aligned with stakeholder expectations  

---

## Implementation
- Data
  - `data/sample/` - Small sample dataset (committed) for quick exploration
  - `data/raw/` - Full dataset (ignored) downloaded via ETL pipeline
- ETL 
  - Set up Kaggle API credentials: `~/.kaggle/kaggle.json`
  - Run ingestion: `python src/etl/ingest_nfl_dataset.py`

---

## Next Steps (Simulated Team Roadmap)

- [x] **Download dataset, place in `data/raw/`** – *Linda, Week 1*  
  (Set up repo structure, gather raw data sources, ensure reproducibility)
- [ ] **Initial exploratory analysis in Jupyter notebooks** – *Ronald, Week 1–2*  
  (EDA, data profiling, highlight potential metrics and anomalies)
- [ ] **Build ETL scripts to populate `data/processed/`** – *Walter, Week 2–3*  
  (Python pipeline, data quality checks, handle anomalies)
- [ ] **Develop SQL queries for core metrics** – *Linda, Week 3*  
  (Model data for analysis, define key business metrics)
- [ ] **Prototype dashboards & document findings** – *Florence, Week 4*  
  (Tableau/Power BI dashboards, stakeholder-facing summary)
- [ ] **Finalize insights & documentation** – *Team, Week 5*  
  (Deliver README, methodology, assumptions, actionable recommendations)

---

## Business Impact & Portfolio Takeaways

- **Stakeholder Alignment:** Simulates iterative feedback loops with leadership, adjusting scope based on data availability  
- **Data Engineering & Analytics Skills:** ETL, SQL modeling, dashboard creation, statistical analysis  
- **Decision Support:** Provides actionable insights for operational planning and fan engagement strategy  
- **Professional Storytelling:** Demonstrates end-to-end analytics workflow, reflecting real-world enterprise scenarios  
