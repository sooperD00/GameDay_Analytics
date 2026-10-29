-- Test: Every 2000-2019 team-season has 16 games, 8 at home, and a record that adds up
-- Returns rows that FAIL
-- Wins and losses come from standings, ties and games from game results, so this also
-- checks the two Kaggle files against each other.

SELECT
    team_season_key,
    games_played,
    home_games_played,
    wins,
    losses,
    ties
FROM {{ ref('int_team_season_performance') }}
WHERE games_played <> 16           -- every season in the Kaggle data had 16 games
   OR home_games_played <> 8
   OR wins + losses + ties <> games_played
   OR games_played IS NULL
