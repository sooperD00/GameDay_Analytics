-- Find team names in kaggle_attendance that don't have a mapping in team_reference
SELECT COUNT(DISTINCT team || ' ' || team_name) 
FROM kaggle_attendance 
WHERE team || ' ' || team_name NOT IN (
    SELECT team_city || ' ' || team_name 
    FROM team_reference
);
