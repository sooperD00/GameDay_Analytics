-- Test: All Kaggle teams must have a mapping in team_reference_seed
-- Returns rows that FAIL (teams without a valid reference mapping)
-- Replaces: sql/validation/unmapped_teams.sql

SELECT
    ka.team_location,
    ka.team_name,
    ka.season_year
FROM {{ ref('stg_kaggle_attendance') }} ka
LEFT JOIN {{ ref('stg_team_reference') }} tr
    ON ka.team_location = tr.team_location
    AND ka.team_name = tr.team_name
    AND CAST(ka.season_year AS TEXT) BETWEEN tr.active_from AND tr.active_to
WHERE tr.espn_team_id IS NULL
GROUP BY ka.team_location, ka.team_name, ka.season_year
