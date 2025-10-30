-- Staging: ESPN Games Score/Wins Data (2020-2024)
-- Grain: One row per game (game_id is unique)
-- Purpose: Extract final scores and win/loss outcomes

WITH source AS (
    SELECT * FROM espn_games_score_wins
),

renamed AS (
    SELECT
        -- Keys
        id AS game_id,
        
        -- Home team
        winner_home AS is_home_winner,
        score_home AS home_final_score,
        
        -- Away team
        winner_away AS is_away_winner,
        score_away AS away_final_score
        
    FROM source
)

SELECT * FROM renamed
