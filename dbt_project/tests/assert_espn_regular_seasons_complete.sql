-- Test: Every ESPN season has all of its regular-season games
-- Returns rows that FAIL (seasons with fewer games than seeds/regular_season_sizes.csv expects)
-- Why: the first ESPN download stopped at 300 events per calendar year and lost 153
--      late-season games, and every other test still passed.

WITH expected AS (
    SELECT season_year, games AS expected_games
    FROM {{ ref('regular_season_sizes') }}
),

actual AS (
    SELECT season_year, COUNT(*) AS actual_games
    FROM {{ ref('stg_espn_games_time') }}
    WHERE season_type = 2
    GROUP BY season_year
)

SELECT
    e.season_year,
    e.expected_games,
    COALESCE(a.actual_games, 0) AS actual_games
FROM expected e
LEFT JOIN actual a
    ON a.season_year = e.season_year
WHERE COALESCE(a.actual_games, 0) < e.expected_games
