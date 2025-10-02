# GameDay Analytics

`GameDay Analytics` is a business-style analytics project analyzing sports/event datasets to simulate real-world insights for stakeholders. The goal is to demonstrate **end-to-end skills in Python ETL, SQL data modeling, dashboards, and actionable reporting**.

### Customers & Stakeholders
- **Primary Stakeholder:** [Jordan Kaplan](https://cod-esports.fandom.com/wiki/JKap), VP of Sports Analytics
- **Use Case:** understand ticket sales trends, attendance patterns, and fan engagement metrics to make marketing and operational decisions.
- **Requirements:** 
  - Reusable, documented data models
  - Automated ETL pipelines
  - SQL-based querying for metrics
  - Dashboards for visualization

### Team Members
- [Walter A. Shewhart](https://en.wikipedia.org/wiki/Walter_A._Shewhart) – Data Quality & Statistical Methods
- [Florence Nightingale](https://en.wikipedia.org/wiki/Florence_Nightingale) – Data Visualization & Dashboarding
- [Ronald A. Fisher](https://en.wikipedia.org/wiki/Ronald_Fisher) – A/B Testing & Analysis
- [Linda B. Low-k-dielectric](www.linkedin.com/in/nicole-rowsey) – ETL Pipeline Development

### Timeline & Milestones
1. **Week 1:** Identify dataset, ingest raw data
2. **Week 2:** Clean, transform, and model data
3. **Week 3:** Build SQL queries, aggregate metrics
4. **Week 4:** Create dashboards, deliver actionable insights
5. **Week 5:** Finalize documentation & repo


### Project Structure
```bash
EventMetrics/
├── README.md               # Project overview, planning notes, instructions
├── requirements.txt        # Python dependencies
├── .gitignore              # Git ignore file
├── data/                   # CSVs, raw data dumps, or SQL scripts for demo datasets
│   ├── raw/
│   └── processed/
├── notebooks/              # Jupyter notebooks for exploration, prototyping, analysis
├── src/                    # Python scripts
│   ├── etl/                # ETL scripts
│   ├── models/             # Data modeling / transformation scripts
│   └── utils/              # Helper functions
├── sql/                    # SQL scripts / queries
├── dashboards/             # Placeholder for Power BI / Tableau dashboards
└── docs/                   # Optional extended documentation
```

## Next Steps
- [ ] **Download dataset, place in `data/raw/`** *Linda, Week 1*
  (Set up repo structure, gather raw data sources, ensure reproducibility)
- [ ] **Start initial exploratory analysis in Jupyter notebooks** *Ronald, Week 1–2*
  (Perform EDA, data profiling, highlight potential metrics and anomalies)
- [ ] **Build ETL scripts to populate `data/processed/`** *Walter, Week 2–3 (in parallel with Ronald)*
  (Develop Python ETL pipeline, incorporate issues surfaced during EDA, enforce data quality checks)
- [ ] **Develop SQL queries for core metrics** *Linda, Week 3*
  (Model data for analysis, define key business metrics, validate outputs)
- [ ] **Prototype dashboards, document findings** *Florence, Week 4*
  (Build dashboard in Tableau/Power BI, draft stakeholder-facing summary)
