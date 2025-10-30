-- Staging: ESPN Games Team Attributes (2020-2024)
-- Grain: One row per game (game_id is unique)
-- Purpose: Extract team branding and identification for both home/away teams

WITH source AS (
    SELECT * FROM espn_games_team_attributes
),

renamed AS (
    SELECT
        -- Keys
        id AS game_id,
        
        -- Game naming
        name AS full_game_name,
        shortName AS short_game_name,
        
        -- Home team
        id_home AS home_team_id,
        team_location_home AS home_team_location,
        team_name_home AS home_team_name,
        team_abbreviation_home AS home_team_abbr,
        team_displayName_home AS home_team_display_name,
        team_color_home AS home_team_primary_color,
        team_logo_home AS home_team_logo_url,
        
        -- Away team
        id_away AS away_team_id,
        team_location_away AS away_team_location,
        team_name_away AS away_team_name,
        team_abbreviation_away AS away_team_abbr,
        team_displayName_away AS away_team_display_name,
        team_color_away AS away_team_primary_color,
        team_logo_away AS away_team_logo_url
        
    FROM source
)

SELECT * FROM renamed
