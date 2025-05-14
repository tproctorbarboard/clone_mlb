import statsapi
import requests
from datetime import datetime, timedelta

def main():
    # Get yesterday's games
    yesterday = datetime.now() - timedelta(days=1)
    date_str = yesterday.strftime("%m/%d/%Y")
    games = statsapi.schedule(start_date=date_str, end_date=date_str)

    if not games:
        print("❌ No games found.")
        return

    # Test first game
    game_id = games[0]["game_id"]
    print(f"🔍 Testing highlights for game ID: {game_id}")

    url = f"https://statsapi.mlb.com/api/v1/game/{game_id}/content"
    try:
        r = requests.get(url)
        r.raise_for_status()
        data = r.json()

        items = data.get("highlights", {}).get("highlights", {}).get("items", [])
        print(f"📹 Found {len(items)} highlight clips")

        # Dump structure of the first 1–2 highlights
        for i, item in enumerate(items[:2]):
            print(f"\n🎞️ Highlight Clip {i+1}:")
            for key, val in item.items():
                if isinstance(val, list):
                    print(f"  {key}: [List of {len(val)} items]")
                elif isinstance(val, dict):
                    print(f"  {key}: {{...}}")
                else:
                    print(f"  {key}: {val}")
                    
            print("-" * 60)

    except Exception as e:
        print(f"⚠️ Error fetching highlights: {e}")

if __name__ == "__main__":
    main()

