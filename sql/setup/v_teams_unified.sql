CREATE VIEW IF NOT EXISTS v_teams_unified AS
SELECT 
    espn_team_id,
    team_city,
    team_name,
    team_city || ' ' || team_name as full_name,
    conference,
    division,
    active_years
FROM team_reference
ORDER BY conference, division, espn_team_id, active_years;
