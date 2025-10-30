-- Staging: ESPN Games Stats Data (2020-2024)
-- Grain: One row per game (game_id is unique)
-- Purpose: Extract quarter-by-quarter scoring and player leaders

WITH source AS (
    SELECT * FROM espn_games_stats_data
),

renamed AS (
    SELECT
        -- Keys
        id AS game_id,
        
        -- Data availability
        playByPlayAvailable AS has_play_by_play,
        
        -- Home team linescores (by quarter/period)
        linescores_value_P1_home AS home_score_q1,
        linescores_value_P2_home AS home_score_q2,
        linescores_value_P3_home AS home_score_q3,
        linescores_value_P4_home AS home_score_q4,
        linescores_value_P5_home AS home_score_ot,
        
        -- Away team linescores
        linescores_value_P1_away AS away_score_q1,
        linescores_value_P2_away AS away_score_q2,
        linescores_value_P3_away AS away_score_q3,
        linescores_value_P4_away AS away_score_q4,
        linescores_value_P5_away AS away_score_ot
        
        -- Note: Player leader stats also available in source
        -- (passing/rushing/receiving leaders with names, jersey numbers)
        -- Omitted for now - add when needed for player performance analysis
        
    FROM source
)

SELECT * FROM renamed
