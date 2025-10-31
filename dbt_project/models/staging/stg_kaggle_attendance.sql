-- Staging: Kaggle Attendance Data (2000-2019)
-- Grain: One row per team per week per season
-- Purpose: Standardize column names, create composite key, filter incomplete records

WITH source AS (
    SELECT * FROM kaggle_attendance
),

renamed AS (
    SELECT
        -- Keys
        team || '_' || team_name || '_' || year || '_' || week AS attendance_key,  --avoids duplicate e.g. Los Angeles_Chargers_2018, Los Angeles_Rams_2018
        team AS team_location,
        team_name,
        year AS season_year,
        week AS week_number,
        
        -- Attendance metrics
        weekly_attendance,
        total AS season_total_attendance,
        home AS season_home_attendance
        
    FROM source
    WHERE weekly_attendance IS NOT NULL  -- Filter out incomplete records
)

SELECT * FROM renamed
