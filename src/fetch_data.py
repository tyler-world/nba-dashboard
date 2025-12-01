import pandas as pd
import os
from nba_api.stats.endpoints import leaguestandings, leagueleaders
from datetime import datetime

SEASON = "2025-26"
SEASON_TYPE = "Regular Season"
PER_MODE = "PerGame"
TOP_N = 25

def fetch_standings():
    df = leaguestandings.LeagueStandings(season=SEASON).get_data_frames()[0]
    df["last_updated"] = datetime.now()
    return df

def fetch_league_leaders(stat):
    df = leagueleaders.LeagueLeaders(
        season=SEASON,
        season_type_all_star=SEASON_TYPE,
        per_mode48=PER_MODE,
        stat_category_abbreviation=stat
    ).get_data_frames()[0]
    df["stat_type"] = stat
    df["last_updated"] = datetime.now()
    return df

def main():
    standings = fetch_standings()
    pts = fetch_league_leaders("PTS").head(TOP_N)
    ast = fetch_league_leaders("AST").head(TOP_N)
    reb = fetch_league_leaders("REB").head(TOP_N)

    standings.to_csv("export/standings.csv", index=False)
    pts.to_csv("export/league_leaders_pts.csv", index=False)
    ast.to_csv("export/league_leaders_ast.csv", index=False)
    reb.to_csv("export/league_leaders_reb.csv", index=False)

    print("CSV exports complete. Files saved in /export")

    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 200)
    pd.set_option('display.colheader_justify', 'center')

    print("\nStandings Sample:")
    print(standings.head())

    print("\nTop Scorers:")
    print(pts.head(20))

    print("\nTop Assists:")
    print(ast.head(20))

    print("\nTop Rebounds:")
    print(reb.head(20))

if __name__ == "__main__":
    main()