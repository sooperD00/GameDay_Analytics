CREATE VIEW IF NOT EXISTS v_attendance_historical AS
SELECT 
    ka.team,
    ka.team_name,
    ka.year,
    ka.week,
    ka.weekly_attendance,
    tr.espn_team_id,
    tr.conference,
    tr.division
FROM kaggle_attendance ka
LEFT JOIN team_reference tr 
    ON ka.team = tr.team_city 
    AND ka.team_name = tr.team_name
    AND CAST(ka.year AS TEXT) BETWEEN 
        SUBSTR(tr.active_years, 1, 4) AND 
        SUBSTR(tr.active_years, -4);