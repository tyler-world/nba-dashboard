import pandas as pd
from nba_api.stats.endpoints import leaguestandings, leagueleaders
from datetime import datetime

# -----------------------------
# Config / Shared Parameters
# -----------------------------
SEASON = "2025-26"
SEASON_TYPE = "Regular Season"
PER_MODE = "PerGame"

# -----------------------------
# Fetch Functions
# -----------------------------
def fetch_standings():
    df = leaguestandings.LeagueStandings(
        season=SEASON,
        season_type=SEASON_TYPE
    ).get_data_frames()[0]
    df["LastUpdated"] = datetime.now()
    df["Season"] = SEASON
    return df

def fetch_league_leaders(stat):
    df = leagueleaders.LeagueLeaders(
        league_id="00",
        per_mode48=PER_MODE,
        scope="S",
        season=SEASON,
        season_type_all_star=SEASON_TYPE,
        stat_category_abbreviation=stat,
        active_flag_nullable=""
    ).get_data_frames()[0]

    df["StatType"] = stat
    df["LastUpdated"] = datetime.now()
    df["Season"] = SEASON
    return df

# -----------------------------
# Export Function for Tableau
# -----------------------------
def export_tableau_csv(df, filename, stat=None):
    df = df.copy()
    
    if stat:
        # Rename the stat column to 'Value' for long format
        df = df.rename(columns={stat: "Value"})
        # Keep only relevant columns
        keep_cols = [
            "Season","PLAYER","PLAYER_ID","TEAM_ID","TEAM_ABBREVIATION",
            "StatType","Value","GP","MIN","LastUpdated"
        ]
        df = df[[c for c in keep_cols if c in df.columns]]
    else:
        # Standings CSV: keep all relevant columns
        keep_cols = [
            "Season","TeamID","TeamName","Conference","ConferenceRecord",
            "PlayoffRank","Wins","Losses","WinPct","LastUpdated"
        ]
        df = df[[c for c in keep_cols if c in df.columns]]

    df.to_csv(f"../data/{filename}.csv", index=False)
    print(f"Exported {filename}.csv for Tableau")

# -----------------------------
# Main Function
# -----------------------------
def main():
    print("Fetching league standings...")
    standings = fetch_standings()
    export_tableau_csv(standings, "standings")

    print("Fetching top scorers...")
    top_pts = fetch_league_leaders("PTS")
    export_tableau_csv(top_pts, "top_pts", stat="PTS")

    print("Fetching top assist leaders...")
    top_ast = fetch_league_leaders("AST")
    export_tableau_csv(top_ast, "top_ast", stat="AST")

    print("Fetching top rebound leaders...")
    top_reb = fetch_league_leaders("REB")
    export_tableau_csv(top_reb, "top_reb", stat="REB")

    print("All data fetched and exported for Tableau successfully!")

# -----------------------------
# Entry Point
# -----------------------------
if __name__ == "__main__":
    main()
