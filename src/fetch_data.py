import pandas as pd
from nba_api.stats.endpoints import leaguestandings, leagueleaders
from datetime import datetime

# Shared config
SEASON = "2025-26"
SEASON_TYPE = "Regular Season"
PER_MODE = "PerGame"

def fetch_standings():
    data = leaguestandings.LeagueStandings().get_data_frames()[0]
    data["last_updated"] = datetime.now()
    return data

def fetch_league_leaders(stat):
    leaders = leagueleaders.LeagueLeaders().get_data_frames()[0]
    leaders["stat_type"] = stat
    leaders["last_updated"] = datetime.now()
    return leaders

def main():
    print("\nFetching league standings...")
    print(fetch_standings().head(15))

    print("\nFetching top scorers...")
    print(fetch_league_leaders("PTS").head(20))

    print("\nFetching top assist leaders...")
    print(fetch_league_leaders("AST").head(20))

    print("\nFetching top rebound leaders...")
    print(fetch_league_leaders("REB").head(20))

    print("\nAll data fetched successfully!")


if __name__ == "__main__":
    main()
