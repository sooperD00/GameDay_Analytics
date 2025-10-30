-- Staging: ESPN Games Venue Data (2020-2024)
-- Grain: One row per game (game_id is unique)
-- Purpose: Extract venue characteristics for location-based analysis

WITH source AS (
    SELECT * FROM espn_games_venue
),

renamed AS (
    SELECT
        -- Keys
        id AS game_id,
        venue_id,
        
        -- Venue details
        venue_fullName AS venue_name,
        venue_address_city AS venue_city,
        venue_address_state AS venue_state,
        venue_indoor AS is_indoor_venue,
        
        -- Team home venues (for reference)
        team_venue_id_home AS home_team_venue_id,
        team_venue_id_away AS away_team_venue_id
        
    FROM source
)

SELECT * FROM renamed
