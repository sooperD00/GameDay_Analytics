-- Staging: ESPN Games Publicity Data (2020-2024)
-- Grain: One row per game (game_id is unique)
-- Purpose: Extract broadcast and headline information for media impact analysis

WITH source AS (
    SELECT * FROM espn_games_publicity
),

renamed AS (
    SELECT
        -- Keys
        id AS game_id,
        
        -- Headlines
        notes_headline AS game_headline,
        headlines_description AS headline_description,
        headlines_shortLinkText AS headline_short_text,
        
        -- Broadcast info
        broadcast AS primary_broadcast_network,
        broadcasts_market_market1 AS broadcast_market_type,
        broadcasts_names_market1_network1 AS broadcast_network_1,
        broadcasts_names_market1_network2 AS broadcast_network_2,
        broadcasts_names_market1_network3 AS broadcast_network_3,
        
        -- Geographic broadcast details
        geoBroadcasts_type_shortName_broadcast1 AS geo_broadcast_type_1,
        geoBroadcasts_market_type_broadcast1 AS geo_market_type_1,
        geoBroadcasts_lang_broadcast1 AS geo_language_1
        
    FROM source
)

SELECT * FROM renamed
