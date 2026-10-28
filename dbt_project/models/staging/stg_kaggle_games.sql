-- Staging: Kaggle Game Results (2000-2019)
-- Grain: One row per regular-season game (game_key is unique)
-- Purpose: Record which team was home each week and how each game ended.
--          stg_kaggle_attendance can't say that on its own: its weekly figure is the
--          crowd at whatever game the team played, home or away.

WITH source AS (
    SELECT * FROM {{ source('raw', 'kaggle_games') }}
),

renamed AS (
    SELECT
        -- Keys
        year || '_' || week || '_' || home_team AS game_key,
        year AS season_year,
        CAST(week AS INTEGER) AS week_number,

        -- Teams (same city/name spelling as stg_kaggle_attendance)
        home_team_city AS home_team_location,
        home_team_name,
        away_team_city AS away_team_location,
        away_team_name,

        -- Result: `tie` holds a team name only when the game ended tied
        winner AS winner_full_name,
        CASE WHEN tie IS NOT NULL THEN 1 ELSE 0 END AS is_tie

    FROM source
    WHERE week GLOB '[0-9]*'  -- regular season; playoff rounds use names ('WildCard', 'Division', ...)
)

SELECT * FROM renamed
