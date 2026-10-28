-- Intermediate: Team Performance with Prior Season Context
-- Grain: One row per team per season
-- Purpose: Calculate year-over-year home attendance changes for playoff momentum analysis.
--          Seasons follow the franchise (franchise_id), so a relocated team keeps its
--          history; is_relocation_season flags its first season under a new city or name.

WITH performance AS (
    SELECT * FROM {{ ref('int_team_season_performance') }}
),

with_lags AS (
    SELECT
        team_season_key,
        franchise_id,
        team_location,
        team_name,
        season_year,

        -- Current season
        wins,
        losses,
        ties,
        win_percentage,
        made_playoffs,
        won_superbowl,
        avg_home_attendance,
        total_home_attendance,
        home_games_played,

        -- Prior season context (using LAG window function)
        LAG(made_playoffs, 1) OVER franchise_seasons AS prior_season_made_playoffs,
        LAG(avg_home_attendance, 1) OVER franchise_seasons AS prior_season_avg_home_attendance,
        LAG(win_percentage, 1) OVER franchise_seasons AS prior_season_win_pct,
        LAG(team_location || ' ' || team_name, 1) OVER franchise_seasons AS prior_season_team_name

    FROM performance
    WINDOW franchise_seasons AS (PARTITION BY franchise_id ORDER BY season_year)
)

SELECT
    *,

    -- First season in a new city or under a new name (Rams 2016, Chargers 2017)
    CASE
        WHEN prior_season_team_name <> team_location || ' ' || team_name THEN 1
        ELSE 0
    END AS is_relocation_season,

    -- Calculate changes
    CASE
        WHEN prior_season_avg_home_attendance IS NOT NULL THEN
            ROUND(
                ((avg_home_attendance - prior_season_avg_home_attendance)
                / prior_season_avg_home_attendance) * 100,
                1
            )
        ELSE NULL
    END AS attendance_pct_change,

    -- Categorize trend
    CASE
        WHEN prior_season_avg_home_attendance IS NULL THEN 'First Season'
        WHEN avg_home_attendance > prior_season_avg_home_attendance THEN 'Increase'
        WHEN avg_home_attendance < prior_season_avg_home_attendance THEN 'Decrease'
        ELSE 'Flat'
    END AS attendance_trend

FROM with_lags
