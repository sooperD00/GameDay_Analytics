"""
ETL Script: ESPN Season Ingestion
Author: Linda B. Low-k-dielectric
Date: Week 1
Purpose: Pull complete NFL regular seasons (2020-2024) from ESPN's public scoreboard API

What the first version's data showed about the scoreboard endpoint:
- dates=YYYY on its own means a calendar year, not a season. It returned preseason,
  regular-season, postseason, and Pro Bowl games from January to December, ignored
  seasontype=2, and stopped at limit=300. Four of the five seasons came back short.
- dates=YYYY&seasontype=2&week=N asks for week N of season YYYY.

So this script asks for one regular-season week at a time, keeps only the events whose
season and season type match, and stops if a season comes back short. Files are saved
only after every season is complete, so a failed run leaves the last good files alone.

To add a season: append it to CURRENT_SEASON_YEARS (src/utils/config.py) and add its
size to dbt_project/seeds/regular_season_sizes.csv.
"""

# Standard library
import csv
import json
import sys
import time

# Third-party
import requests

# Local
from src.utils.logging_config import setup_logger
from src.utils.config import (
    RAW_DATA_PATH,
    ESPN_TEAMS_URL,
    ESPN_SCOREBOARD_URL,
    CURRENT_SEASON_YEARS,
    SEASON_SIZES_FILE,
)

# Logger
logger = setup_logger(__name__)

REQUEST_TIMEOUT = 30        # seconds to wait on any one request
RETRIES = 3                 # attempts per request before giving up
PAUSE_BETWEEN_CALLS = 0.25  # seconds; a full run makes about 90 week requests
REGULAR_SEASON = 2          # ESPN season types: 1 = pre, 2 = regular, 3 = post


def main():
    """Fetch every regular-season game for CURRENT_SEASON_YEARS and save them as JSON."""
    logger.info("Starting ESPN season ingestion")

    try:
        ensure_directories()
        season_sizes = load_season_sizes()
        teams = fetch_teams()
        games = []
        for season in CURRENT_SEASON_YEARS:
            games.extend(fetch_regular_season(season, *season_sizes[season]))

        save_data(teams, "espn_teams.json")
        save_data(games, "espn_games.json")
    except Exception:
        logger.exception("ESPN ingestion failed; existing files left unchanged")
        sys.exit(1)

    logger.info(f"ESPN ingestion complete: {len(games)} regular-season games")

def ensure_directories():
    """Create necessary directories."""
    RAW_DATA_PATH.mkdir(parents=True, exist_ok=True)
    logger.debug(f"Ensured directory exists: {RAW_DATA_PATH}")

def load_season_sizes():
    """Read weeks and game counts per season from the dbt seed (shared with the dbt tests)."""
    with open(SEASON_SIZES_FILE, newline="") as f:
        sizes = {
            int(row["season_year"]): (int(row["weeks"]), int(row["games"]))
            for row in csv.DictReader(f)
        }
    missing = [season for season in CURRENT_SEASON_YEARS if season not in sizes]
    if missing:
        raise ValueError(f"No row in {SEASON_SIZES_FILE.name} for seasons {missing}")
    return sizes

def get_json(url, params=None):
    """GET a URL and return its JSON, retrying transient failures."""
    for attempt in range(1, RETRIES + 1):
        try:
            response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            if attempt == RETRIES:
                raise
            wait = 2 ** attempt
            logger.warning(f"  {e} (attempt {attempt}/{RETRIES}, retrying in {wait}s)")
            time.sleep(wait)

def fetch_teams():
    """Fetch NFL team data from ESPN API."""
    logger.info("Fetching teams from ESPN API")

    data = get_json(ESPN_TEAMS_URL)
    teams = data['sports'][0]['leagues'][0]['teams']

    logger.info(f"Retrieved {len(teams)} teams")
    return teams

def fetch_regular_season(season, weeks, expected_games):
    """Fetch one regular season a week at a time; stop if any games are missing."""
    logger.info(f"Fetching the {season} regular season ({weeks} weeks)")
    games = {}

    for week in range(1, weeks + 1):
        params = {"dates": season, "seasontype": REGULAR_SEASON, "week": week}
        for event in get_json(ESPN_SCOREBOARD_URL, params).get("events", []):
            # The request already asks for this season and type. Checking again is
            # cheap insurance, since the old year-only request ignored seasontype.
            if event["season"]["year"] == season and event["season"]["type"] == REGULAR_SEASON:
                games[event["id"]] = event  # keyed by id, so a repeated event counts once
        time.sleep(PAUSE_BETWEEN_CALLS)

    if len(games) < expected_games:
        raise ValueError(
            f"{season}: got {len(games)} regular-season games, expected {expected_games}"
        )
    if len(games) > expected_games:
        logger.warning(
            f"  {season}: {len(games)} games, {len(games) - expected_games} more than expected "
            f"(a canceled game ESPN still lists?)"
        )
    logger.info(f"  {season}: {len(games)} games")
    return list(games.values())

def save_data(data, filename):
    """Save data to JSON file, replacing the old file only once the new one is written."""
    output_file = RAW_DATA_PATH / filename
    tmp_file = output_file.with_name(output_file.name + ".tmp")

    with open(tmp_file, 'w') as f:
        json.dump(data, f, indent=2)
    tmp_file.replace(output_file)

    logger.info(f"Saved data to {output_file}")

if __name__ == "__main__":
    main()
