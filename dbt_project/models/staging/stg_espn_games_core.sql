-- Staging: ESPN Games Core Data (2020-2024)
-- Grain: One row per game (game_id is unique)
-- Purpose: Clean core game attributes and attendance metrics

WITH source AS (
    SELECT * FROM espn_games_core
),

renamed AS (
    SELECT
        -- Keys
        id AS game_id,
        
        -- Attendance
        attendance,
        
        -- Game attributes
        type_abbreviation AS game_type,
        neutralSite AS is_neutral_site,
        team_isActive_home AS is_home_team_active,
        team_isActive_away AS is_away_team_active,
        format_regulation_periods AS regulation_periods
        
    FROM source
    WHERE attendance > 0  -- Filter out games with missing attendance
)

SELECT * FROM renamed
