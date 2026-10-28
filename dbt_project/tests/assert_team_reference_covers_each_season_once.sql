-- Test: team_reference_seed has exactly one row per franchise per season
-- Returns rows that FAIL:
--   overlap  two rows claim the same franchise-season (the as-of join would double that season)
--   gap      no row for a season between the franchise's first season and the last ESPN season
-- Seasons run from the first Kaggle season to the last season in regular_season_sizes.csv,
-- so adding a season there also checks the seed covers it.

WITH RECURSIVE seasons(season_year) AS (
    SELECT MIN(season_year) FROM {{ ref('stg_kaggle_standings') }}
    UNION ALL
    SELECT season_year + 1 FROM seasons
    WHERE season_year < (SELECT MAX(season_year) FROM {{ ref('regular_season_sizes') }})
),

coverage AS (
    SELECT tr.espn_team_id, s.season_year, COUNT(*) AS rows_covering
    FROM seasons s
    JOIN {{ ref('stg_team_reference') }} tr
        ON CAST(s.season_year AS TEXT) BETWEEN tr.active_from AND tr.active_to
    GROUP BY tr.espn_team_id, s.season_year
),

first_seasons AS (
    SELECT espn_team_id, MIN(CAST(active_from AS INTEGER)) AS first_season
    FROM {{ ref('stg_team_reference') }}
    GROUP BY espn_team_id
)

SELECT espn_team_id, season_year, 'overlap: ' || rows_covering || ' rows' AS problem
FROM coverage
WHERE rows_covering > 1

UNION ALL

SELECT f.espn_team_id, s.season_year, 'gap: no row' AS problem
FROM first_seasons f
JOIN seasons s
    ON s.season_year >= f.first_season
LEFT JOIN coverage c
    ON c.espn_team_id = f.espn_team_id
    AND c.season_year = s.season_year
WHERE c.espn_team_id IS NULL
