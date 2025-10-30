-- Intermediate: Team Performance with Attendance
-- Grain: One row per team per season
-- Purpose: Join standings with aggregated attendance for win-attendance correlation

WITH standings AS (
    SELECT * FROM {{ ref('stg_kaggle_standings') }}
),

attendance_agg AS (
    SELECT
        team_location,
        team_name,
        season_year,
        SUM(weekly_attendance) AS total_weekly_attendance,
        AVG(weekly_attendance) AS avg_weekly_attendance,
        COUNT(*) AS home_games_played
    FROM {{ ref('stg_kaggle_attendance') }}
    GROUP BY team_location, team_name, season_year
)

SELECT
    s.team_season_key,
    s.team_location,
    s.team_name,
    s.season_year,
    
    -- Performance
    s.wins,
    s.losses,
    s.games_played,
    s.win_percentage,
    s.made_playoffs,
    s.won_superbowl,
    s.points_for,
    s.points_against,
    s.margin_of_victory,
    
    -- Attendance
    a.total_weekly_attendance,
    a.avg_weekly_attendance,
    a.home_games_played

FROM standings s
LEFT JOIN attendance_agg a
    ON s.team_location = a.team_location
    AND s.team_name = a.team_name
    AND s.season_year = a.season_year
