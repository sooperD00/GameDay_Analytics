-- Mart: Playoff Momentum Effect
-- Question: Do playoff teams get an attendance boost the following season?
-- Grain: One row per team per season (with prior season data)
-- Purpose: Analyze year-over-year attendance changes after playoff appearances

WITH playoff_context AS (
    SELECT * FROM {{ ref('int_playoff_lag') }}
)

SELECT
    team_season_key,
    franchise_id,
    team_location,
    team_name,
    season_year,

    -- Current season
    wins,
    ties,
    win_percentage,
    made_playoffs,
    won_superbowl,
    avg_home_attendance,
    home_games_played,

    -- Prior season context
    prior_season_made_playoffs,
    prior_season_avg_home_attendance,
    prior_season_win_pct,
    is_relocation_season,  -- kept in; filter on it to leave out new-stadium seasons

    -- Year-over-year change in home attendance
    attendance_pct_change,
    attendance_trend
    
    -- TODO (Linda→Ronald): Add "playoff bump" flag and statistical significance tests
    -- Placeholder for: has_playoff_bump (boolean), expected_vs_actual_attendance
    -- Waiting on notebook 03 to determine threshold for "meaningful" boost (5%? 10%?)
    
FROM playoff_context
WHERE prior_season_avg_home_attendance IS NOT NULL  -- Need prior year data for comparison
