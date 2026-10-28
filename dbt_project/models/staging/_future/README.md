# Future Staging Models (parked)

These staging models are written but **parked**: `dbt_project.yml` sets
`+enabled: false` on this folder, so dbt parses them and doesn't build them.

## Why they exist
The ESPN JSON was decomposed into 7 themed tables (see `notebooks/02_view_design.ipynb`).
For the initial 3 analytical questions, only `core`, `venue`, and `time` tables are needed.
These four cover the other themes for later questions.

## How to activate
1. Move the `.sql` file up to `models/staging/`
2. Add its columns and tests to `models/staging/_staging.yml` (a `unique` test on `game_id` is enough to make `dbt build` query every column)
3. Run `dbt build`

## Available models

### stg_espn_games_publicity.sql
**Use for:** Broadcast impact analysis, headline excitement scoring
**Key fields:** broadcast networks, game headlines, market type (national/local)

### stg_espn_games_score_wins.sql
**Use for:** Win/loss analysis, score differential
**Key fields:** winner flags, final scores for home/away

### stg_espn_games_stats_data.sql
**Use for:** Quarter-by-quarter scoring, overtime games
**Key fields:** linescores by period (player leaders are in the raw JSON but not loaded yet)

### stg_espn_games_team_attributes.sql
**Use for:** Team branding analysis, color psychology, logo recognition
**Key fields:** team names/locations, colors, logos for both home/away

## Example future questions
- Does national broadcast (ESPN/ABC) drive attendance compared to local coverage?
- Do overtime games boost attendance for the next home game?
- Does star quarterback performance correlate with ticket sales?
- Do teams with "exciting" colors (red/orange) draw more fans?
