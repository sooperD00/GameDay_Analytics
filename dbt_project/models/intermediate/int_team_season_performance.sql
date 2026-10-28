-- Intermediate: Team Performance with Home Attendance
-- Grain: One row per team per season (2000-2019)
-- Purpose: Join standings with home-game attendance for the win-attendance question,
--          and attach the franchise id from the team reference seed. That join is an
--          as-of join: it picks the seed row whose active years include the season,
--          so St. Louis Rams 2015 and Los Angeles Rams 2016 get the same franchise id.

WITH standings AS (
    SELECT * FROM {{ ref('stg_kaggle_standings') }}
),

season_games AS (
    SELECT
        team_location,
        team_name,
        season_year,
        COUNT(*) AS games_played,
        SUM(CASE WHEN result = 'T' THEN 1 ELSE 0 END) AS ties,
        SUM(is_home) AS home_games_played,
        SUM(CASE WHEN is_home = 1 THEN attendance END) AS total_home_attendance,
        AVG(CASE WHEN is_home = 1 THEN attendance END) AS avg_home_attendance
    FROM {{ ref('int_kaggle_team_games') }}
    GROUP BY team_location, team_name, season_year
),

team_reference AS (
    SELECT * FROM {{ ref('stg_team_reference') }}
)

SELECT
    s.team_season_key,
    tr.espn_team_id AS franchise_id,
    s.team_location,
    s.team_name,
    s.season_year,

    -- Performance
    s.wins,
    s.losses,
    g.ties,
    g.games_played,
    ROUND((s.wins + 0.5 * g.ties) / g.games_played, 3) AS win_percentage,  -- a tie counts as half a win
    s.made_playoffs,
    s.won_superbowl,
    s.points_for,
    s.points_against,
    s.margin_of_victory,

    -- Attendance at the team's own home games
    g.home_games_played,
    g.total_home_attendance,
    g.avg_home_attendance

FROM standings s
LEFT JOIN season_games g
    ON s.team_location = g.team_location
    AND s.team_name = g.team_name
    AND s.season_year = g.season_year
LEFT JOIN team_reference tr
    ON s.team_location = tr.team_location
    AND s.team_name = tr.team_name
    AND CAST(s.season_year AS TEXT) BETWEEN tr.active_from AND tr.active_to
