import statsapi
import requests
from datetime import datetime, timedelta

def main():
    # Get yesterday's date and fetch games
    yesterday = datetime.now() - timedelta(days=1)
    date_str = yesterday.strftime("%m/%d/%Y")
    games = statsapi.schedule(start_date=date_str, end_date=date_str)

    if not games:
        print("❌ No games found.")
        return

    game_id = games[0]["game_id"]
    print(f"🔍 Checking keywordsAll for game ID: {game_id}")

    url = f"https://statsapi.mlb.com/api/v1/game/{game_id}/content"
    r = requests.get(url)
    r.raise_for_status()
    content = r.json()

    highlights = content.get("highlights", {}).get("highlights", {}).get("items", [])
    print(f"📹 Found {len(highlights)} highlight items")

    # Try parsing person names and IDs
    for i, clip in enumerate(highlights[:5]):
        print(f"\n🎞️ Clip {i+1}: {clip.get('headline', 'No Headline')}")
        keywords = clip.get("keywordsAll", [])
        for kw in keywords:
            if kw.get("type") == "person_id":
                print(f"  👤 {kw.get('displayName', 'Unknown')} (ID: {kw.get('value')})")

if __name__ == "__main__":
    main()

