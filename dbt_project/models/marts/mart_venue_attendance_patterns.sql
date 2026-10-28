-- Mart: Venue Attendance Patterns
-- Question: Does venue type (indoor/outdoor) affect attendance patterns?
-- Grain: One row per venue (aggregated across its regular-season games, 2021-2024)
-- Purpose: Compare attendance stability and averages across venue characteristics
-- Scope: 2020 is left out. COVID rules kept most stadiums empty or capped that year,
--        and those games, not weather, set nearly every venue's minimum crowd.

WITH games_combined AS (
    SELECT
        c.game_id,
        c.attendance,
        v.venue_id,
        v.venue_name,
        v.venue_city,
        v.venue_state,
        v.is_indoor_venue,
        t.season_year,
        t.week_number
    FROM {{ ref('stg_espn_games_core') }} c
    JOIN {{ ref('stg_espn_games_venue') }} v
        ON c.game_id = v.game_id
    JOIN {{ ref('stg_espn_games_time') }} t
        ON c.game_id = t.game_id
    WHERE t.season_type = 2        -- regular season only (no preseason, playoffs, or Pro Bowl)
      AND t.season_year >= 2021    -- see Scope above
      AND c.attendance > 0         -- drops games with no reported attendance
),

venue_stats AS (
    SELECT
        venue_id,
        venue_name,
        venue_city,
        venue_state,
        is_indoor_venue,
        
        -- Attendance aggregates
        COUNT(*) AS games_played,
        AVG(attendance) AS avg_attendance,
        MIN(attendance) AS min_attendance,
        MAX(attendance) AS max_attendance,
        
        -- Variability metrics
        -- Note: SQLite doesn't have STDDEV, using range as proxy
        (MAX(attendance) - MIN(attendance)) AS attendance_range,
        ROUND(
            ((MAX(attendance) - MIN(attendance)) / AVG(attendance)) * 100,
            1
        ) AS attendance_variability_pct
        
    FROM games_combined
    GROUP BY venue_id, venue_name, venue_city, venue_state, is_indoor_venue
)

SELECT
    *,
    
    -- Categorize venue type
    CASE
        WHEN is_indoor_venue = 1 THEN 'Indoor'
        ELSE 'Outdoor'
    END AS venue_type
    
    -- TODO (Linda→Ronald): Add weather data join for outdoor venues
    -- Placeholder for: avg_temp, precipitation_days, weather_impact_score
    -- Would enable: "Do outdoor venues in cold climates show higher variability?"
    
FROM venue_stats
WHERE games_played >= 5  -- Only venues with sufficient game sample
