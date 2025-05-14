import requests

def fetch_player_stats(player_id):
    """
    Fetch 2025 season stats for a player.
    """
    season_year = "2025"
    url = f"https://statsapi.mlb.com/api/v1/people/{player_id}/stats?stats=season&season={season_year}"
    response = requests.get(url)
    data = response.json()

    if "stats" in data and data["stats"]:
        splits = data["stats"][0]["splits"]
        if splits:
            return splits[0]["stat"]
    return {}

