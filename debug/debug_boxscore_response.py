import requests

# Use a real game ID from your event list
game_id = 745803  # Replace with the game ID from the failed case if needed
url = f"https://statsapi.mlb.com/api/v1/game/{game_id}/boxscore"

try:
    r = requests.get(url)
    r.raise_for_status()
    boxscore = r.json()
    
    print("🔍 Top-level keys in boxscore JSON:")
    print(list(boxscore.keys()))

    print("\n📥 Raw response for inspection:")
    from pprint import pprint
    pprint(boxscore)

except Exception as e:
    print(f"❌ Error fetching boxscore: {e}")


