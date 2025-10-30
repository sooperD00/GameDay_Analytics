-- Staging: Kaggle Attendance Data (2000-2019)
-- Grain: One row per team per week per season
-- Purpose: Standardize column names, create composite key, filter incomplete records

WITH source AS (
    SELECT * FROM kaggle_attendance
),

renamed AS (
    SELECT
        -- Keys
        team || '_' || year || '_' || week AS attendance_key,
        team AS team_location,
        team_name,
        year AS season_year,
        week AS week_number,
        
        -- Attendance metrics
        weekly_attendance,
        total_attendance AS season_total_attendance,
        home_attendance AS season_home_attendance
        
    FROM source
    WHERE weekly_attendance IS NOT NULL  -- Filter out incomplete records
)

SELECT * FROM renamed
