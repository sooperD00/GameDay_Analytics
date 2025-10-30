-- Staging: ESPN Games Time Data (2020-2024)
-- Grain: One row per game (game_id is unique)
-- Purpose: Extract temporal attributes for time-based analysis and joining

WITH source AS (
    SELECT * FROM espn_games_time
),

renamed AS (
    SELECT
        -- Keys
        id AS game_id,
        
        -- Season context
        season_year,
        season_type,
        season_slug,
        week_number,
        
        -- Timestamps
        date AS game_date,
        startDate AS game_start_datetime
        
    FROM source
)

SELECT * FROM renamed
