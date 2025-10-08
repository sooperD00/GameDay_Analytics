"""
ETL Script: Current Season Data Ingestion
Author: Linda B. Low-k-dielectric
Date: Week 1
Purpose: Pull current NFL season data (2020-2024) from ESPN API
"""

# Standard library
import json
from pathlib import Path
from datetime import datetime

# Third-party
import requests

# Local
from src.utils.logging_config import setup_logger

# Constants
RAW_DATA_PATH = Path(__file__).parent.parent.parent / "data" / "raw"
ESPN_TEAMS_URL = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams"
ESPN_SCOREBOARD_BASE = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"

# Logger
logger = setup_logger(__name__)

def main():
    """Fetch current season NFL data from ESPN API."""
    logger.info("Starting current season data ingestion from ESPN")
    
    ensure_directories()
    teams = fetch_teams()
    games = fetch_games_for_seasons([2020, 2021, 2022, 2023, 2024])
    
    save_data(teams, "espn_teams.json")
    save_data(games, "espn_games.json")
    
    logger.info("Current season ingestion complete")

def ensure_directories():
    """Create necessary directories."""
    RAW_DATA_PATH.mkdir(parents=True, exist_ok=True)
    logger.debug(f"Ensured directory exists: {RAW_DATA_PATH}")

def fetch_teams():
    """Fetch NFL team data from ESPN API."""
    logger.info(f"Fetching teams from ESPN API")
    
    response = requests.get(ESPN_TEAMS_URL)
    response.raise_for_status()
    
    data = response.json()
    teams = data['sports'][0]['leagues'][0]['teams']
    
    logger.info(f"Retrieved {len(teams)} teams")
    return teams

def fetch_games_for_seasons(years):
    """
    Fetch game data for multiple seasons.
    Note: ESPN API has rate limits - using basic approach for portfolio demo.
    """
    all_games = []
    
    for year in years:
        logger.info(f"Fetching games for {year} season")
        
        # Get regular season games (seasontype=2)
        url = f"{ESPN_SCOREBOARD_BASE}?dates={year}&seasontype=2&limit=300"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if 'events' in data:
                games = data['events']
                all_games.extend(games)
                logger.info(f"  Retrieved {len(games)} games for {year}")
        except Exception as e:
            logger.error(f"Error fetching {year} season: {e}")
    
    logger.info(f"Total games retrieved: {len(all_games)}")
    return all_games

def save_data(data, filename):
    """Save data to JSON file."""
    output_file = RAW_DATA_PATH / filename
    
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    logger.info(f"Saved data to {output_file}")

if __name__ == "__main__":
    main()