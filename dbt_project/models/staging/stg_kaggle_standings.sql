-- Staging: Kaggle Standings Data (2000-2019)
-- Grain: One row per team per season
-- Purpose: Clean performance metrics, create playoff flags
--          (no ties column here: games played and win percentage come from game
--          results in int_team_season_performance)

WITH source AS (
    SELECT * FROM {{ source('raw', 'kaggle_standings') }}
),

renamed AS (
    SELECT
        -- Keys
        team || '_' || team_name || '_' || year AS team_season_key, --avoids duplicate e.g. Los Angeles_Chargers_2018, Los Angeles_Rams_2018
        team AS team_location,
        team_name,
        year AS season_year,
        
        -- Performance metrics
        wins,
        loss AS losses,

        -- Scoring
        points_for,
        points_against,
        points_differential,
        margin_of_victory,
        
        -- Advanced stats
        strength_of_schedule,
        simple_rating,
        offensive_ranking,
        defensive_ranking,
        
        -- Playoff indicators
        CASE 
            WHEN playoffs = 'Playoffs' THEN 1 
            ELSE 0 
        END AS made_playoffs,
        
        CASE 
            WHEN sb_winner != 'No Superbowl' THEN 1 
            ELSE 0 
        END AS won_superbowl

    FROM source
)

SELECT * FROM renamed
