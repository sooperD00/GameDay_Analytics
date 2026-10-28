-- Test: The three Kaggle files describe the same seasons and games
-- Returns rows that FAIL:
--   standings without attendance / attendance without standings
--       (int_team_season_performance starts from standings, so attendance for a
--        team-season with no standings row would silently drop out of the marts)
--   attendance without a game
--       (a weekly attendance figure that matches no game that team played that week)

WITH standings AS (
    SELECT DISTINCT team_location, team_name, season_year FROM {{ ref('stg_kaggle_standings') }}
),

attendance AS (
    SELECT DISTINCT team_location, team_name, season_year FROM {{ ref('stg_kaggle_attendance') }}
)

SELECT s.team_location, s.team_name, s.season_year, NULL AS week_number,
       'standings without attendance' AS problem
FROM standings s
LEFT JOIN attendance a USING (team_location, team_name, season_year)
WHERE a.team_location IS NULL

UNION ALL

SELECT a.team_location, a.team_name, a.season_year, NULL AS week_number,
       'attendance without standings' AS problem
FROM attendance a
LEFT JOIN standings s USING (team_location, team_name, season_year)
WHERE s.team_location IS NULL

UNION ALL

SELECT ka.team_location, ka.team_name, ka.season_year, ka.week_number,
       'attendance without a game' AS problem
FROM {{ ref('stg_kaggle_attendance') }} ka
LEFT JOIN {{ ref('int_kaggle_team_games') }} tg
    ON tg.team_location = ka.team_location
    AND tg.team_name = ka.team_name
    AND tg.season_year = ka.season_year
    AND tg.week_number = ka.week_number
WHERE tg.team_game_key IS NULL
