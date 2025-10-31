-- Intermediate: Team Performance with Prior Season Context
-- Grain: One row per team per season
-- Purpose: Calculate year-over-year changes for playoff momentum analysis

WITH performance AS (
    SELECT * FROM {{ ref('int_team_season_performance') }}
),

with_lags AS (
    SELECT
        team_season_key,
        team_location,
        team_name,
        season_year,
        
        -- Current season
        wins,
        losses,
        win_percentage,
        made_playoffs,
        won_superbowl,
        avg_weekly_attendance,
        total_weekly_attendance,
        home_games_played,
        
        -- Prior season context (using LAG window function)
        LAG(made_playoffs, 1) OVER (
            PARTITION BY team_location, team_name 
            ORDER BY season_year
        ) AS prior_season_made_playoffs,
        
        LAG(avg_weekly_attendance, 1) OVER (
            PARTITION BY team_location, team_name 
            ORDER BY season_year
        ) AS prior_season_avg_attendance,
        
        LAG(win_percentage, 1) OVER (
            PARTITION BY team_location, team_name 
            ORDER BY season_year
        ) AS prior_season_win_pct
        
    FROM performance
)

SELECT
    *,
    
    -- Calculate changes
    CASE 
        WHEN prior_season_avg_attendance IS NOT NULL THEN
            ROUND(
                ((avg_weekly_attendance - prior_season_avg_attendance) 
                / prior_season_avg_attendance) * 100, 
                1
            )
        ELSE NULL
    END AS attendance_pct_change,
    
    -- Categorize trend
    CASE
        WHEN prior_season_avg_attendance IS NULL THEN 'First Season'
        WHEN avg_weekly_attendance > prior_season_avg_attendance THEN 'Increase'
        WHEN avg_weekly_attendance < prior_season_avg_attendance THEN 'Decrease'
        ELSE 'Flat'
    END AS attendance_trend

FROM with_lags
