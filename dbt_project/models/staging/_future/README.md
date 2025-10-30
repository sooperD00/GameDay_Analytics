# Future Staging Models

These staging models are **ready to use** but not yet included in the active dbt pipeline.

## Why they exist
The ESPN JSON was decomposed into 7 themed tables (see `notebooks/02_view_design.ipynb`). 
For the initial 3 analytical questions, only `core`, `venue`, and `time` tables are needed.
These remaining models are production-ready for future analysis questions.

## How to activate
1. Move desired `.sql` file(s) up to `models/staging/`
2. Add documentation in `models/staging/_staging.yml`
3. Run `dbt run`

## Available models

### stg_espn_games_publicity.sql
**Use for:** Broadcast impact analysis, headline excitement scoring
**Key fields:** broadcast networks, game headlines, market type (national/local)

### stg_espn_games_score_wins.sql  
**Use for:** Win/loss analysis, score differential
**Key fields:** winner flags, final scores for home/away

### stg_espn_games_stats_data.sql
**Use for:** Player performance correlation, quarter-by-quarter scoring, overtime games
**Key fields:** linescores by period, passing/rushing/receiving leaders

### stg_espn_games_team_attributes.sql
**Use for:** Team branding analysis, color psychology, logo recognition
**Key fields:** team names/locations, colors, logos for both home/away

## Example future questions
- Does national broadcast (ESPN/ABC) drive attendance compared to local coverage?
- Do overtime games boost attendance for the next home game?
- Does star quarterback performance correlate with ticket sales?
- Do teams with "exciting" colors (red/orange) draw more fans?
