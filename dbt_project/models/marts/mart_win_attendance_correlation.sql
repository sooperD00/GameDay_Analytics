-- Mart: Win-Attendance Correlation Analysis
-- Question: Does winning drive attendance?
-- Grain: One row per team per season
-- Purpose: Analysis-ready table showing relationship between team performance and attendance

WITH performance AS (
    SELECT * FROM {{ ref('int_team_season_performance') }}
)

SELECT
    team_season_key,
    franchise_id,
    team_location,
    team_name,
    season_year,

    -- Performance metrics
    wins,
    losses,
    ties,
    win_percentage,
    made_playoffs,
    won_superbowl,

    -- Attendance at the team's own home games
    avg_home_attendance,
    total_home_attendance,
    home_games_played
    
    -- TODO (Linda→Ronald): Add attendance categorization after venue capacity analysis
    -- Placeholder for: attendance_pct_of_capacity, attendance_category, performance_tier
    -- Waiting on notebook 03 EDA to determine appropriate thresholds/groupings
    
FROM performance
WHERE avg_home_attendance IS NOT NULL  -- Only seasons with attendance data
