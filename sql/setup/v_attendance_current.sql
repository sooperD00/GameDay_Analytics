CREATE VIEW IF NOT EXISTS v_attendance_current AS
SELECT 
    eg.id as game_id,
    eg.date,
    eg.season as year,
    eg.week,
    eg.attendance,
    eg.venue_name,
    eg.venue_city
FROM espn_games eg
WHERE eg.attendance > 0;
