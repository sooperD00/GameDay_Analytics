-- Intermediate: Team Games (2000-2019)
-- Grain: One row per team per regular-season game (two rows per game)
-- Purpose: Mark each game as home or away for each team, with its result and its crowd.
--          is_home is what lets the season models average home crowds only.

WITH games AS (
    SELECT * FROM {{ ref('stg_kaggle_games') }}
),

attendance AS (
    SELECT * FROM {{ ref('stg_kaggle_attendance') }}
),

team_games AS (
    SELECT
        game_key, season_year, week_number,
        home_team_location AS team_location,
        home_team_name AS team_name,
        1 AS is_home,
        winner_full_name, is_tie
    FROM games

    UNION ALL

    SELECT
        game_key, season_year, week_number,
        away_team_location AS team_location,
        away_team_name AS team_name,
        0 AS is_home,
        winner_full_name, is_tie
    FROM games
)

SELECT
    -- Keys (same format as stg_kaggle_attendance.attendance_key)
    tg.team_location || '_' || tg.team_name || '_' || tg.season_year || '_' || tg.week_number AS team_game_key,
    tg.game_key,
    tg.team_location,
    tg.team_name,
    tg.season_year,
    tg.week_number,

    -- Game
    tg.is_home,
    CASE
        WHEN tg.is_tie = 1 THEN 'T'
        WHEN tg.winner_full_name = tg.team_location || ' ' || tg.team_name THEN 'W'
        ELSE 'L'
    END AS result,

    -- The crowd at this game, wherever it was played
    a.weekly_attendance AS attendance

FROM team_games tg
LEFT JOIN attendance a
    ON a.team_location = tg.team_location
    AND a.team_name = tg.team_name
    AND a.season_year = tg.season_year
    AND a.week_number = tg.week_number
