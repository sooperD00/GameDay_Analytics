-- Test: Every ESPN team in a regular-season game has a team_reference_seed row for that season
-- Returns rows that FAIL (team ids with no seed row active that season)
-- The ESPN-side twin of assert_kaggle_teams_have_reference_mapping. It used to be a log line
-- in create_team_reference.py, and that only checked the current team list, not each season.
-- Reads the raw team table: its staging model is parked in models/staging/_future/.

WITH game_teams AS (
    SELECT t.season_year, CAST(a.id_home AS INTEGER) AS espn_team_id
    FROM {{ source('raw', 'espn_games_team_attributes') }} a
    JOIN {{ ref('stg_espn_games_time') }} t ON t.game_id = a.id
    WHERE t.season_type = 2

    UNION

    SELECT t.season_year, CAST(a.id_away AS INTEGER) AS espn_team_id
    FROM {{ source('raw', 'espn_games_team_attributes') }} a
    JOIN {{ ref('stg_espn_games_time') }} t ON t.game_id = a.id
    WHERE t.season_type = 2
)

SELECT
    gt.season_year,
    gt.espn_team_id
FROM game_teams gt
LEFT JOIN {{ ref('stg_team_reference') }} tr
    ON gt.espn_team_id = tr.espn_team_id
    AND CAST(gt.season_year AS TEXT) BETWEEN tr.active_from AND tr.active_to
WHERE tr.espn_team_id IS NULL
