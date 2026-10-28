-- Staging: ESPN Games Core Data (2020-2024)
-- Grain: One row per game (game_id is unique)
-- Purpose: Clean core game attributes and attendance metrics
-- Attendance: NULL = ESPN didn't report it; 0 = no fans admitted (most of 2020).
--             Both stay here; each mart decides which games its question needs.

WITH source AS (
    SELECT * FROM {{ source('raw', 'espn_games_core') }}
),

renamed AS (
    SELECT
        -- Keys
        id AS game_id,
        
        -- Attendance (integer even when a missing value made the raw column REAL)
        CAST(attendance AS INTEGER) AS attendance,
        
        -- Game attributes
        type_abbreviation AS game_type,
        neutralSite AS is_neutral_site,
        team_isActive_home AS is_home_team_active,
        team_isActive_away AS is_away_team_active,
        format_regulation_periods AS regulation_periods
        
    FROM source
)

SELECT * FROM renamed
