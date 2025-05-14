# odds/live_tracker.py

import requests

def get_game_stats(gamePk):
    """
    Fetch live game stats from the MLB Stats API.
    Tracks total number of strikeouts and home runs so far.
    """
    url = f"https://statsapi.mlb.com/api/v1.1/game/{gamePk}/feed/live"
    response = requests.get(url)
    response.raise_for_status()  # Raise error if request fails
    live_data = response.json()

    stats = {
        "strikeouts": 0,
        "home_runs": 0
    }

    try:
        all_plays = live_data['liveData']['plays']['allPlays']
    except KeyError:
        print("[ERROR] Could not parse plays from live data.")
        return stats

    for play in all_plays:
        event = play['result'].get('eventType', '')
        if event == 'strikeout':
            stats["strikeouts"] += 1
        elif event == 'home_run':
            stats["home_runs"] += 1

    return stats

