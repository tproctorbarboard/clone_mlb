import statsapi
from datetime import datetime, timedelta
import requests
from trivia_generation.generate_questions import generate_trivia_question

def main():
    print("MLB Trivia Generator started...")
    print("Checking yesterday's games for highlights...\n")

    # Get yesterday's date
    yesterday = datetime.now() - timedelta(days=1)
    date_str = yesterday.strftime("%m/%d/%Y")

    # Get list of games
    games = statsapi.schedule(start_date=date_str, end_date=date_str)
    print(f"🔍 Found {len(games)} games on {date_str}\n")

    if not games:
        print("❌ No games found.")
        return

    for game in games:
        game_id = game.get("game_id")
        if not game_id:
            continue

        print(f"🔍 Processing game ID: {game_id}")
        content_url = f"https://statsapi.mlb.com/api/v1/game/{game_id}/content"

        try:
            response = requests.get(content_url)
            response.raise_for_status()
            content = response.json()

            highlights = content.get("highlights", {}).get("highlights", {}).get("items", [])
            print(f"📹 Found {len(highlights)} highlight items for game {game_id}")

            for clip in highlights:
                desc = clip.get("blurb", "")
                if not desc or "home run" not in desc.lower():
                    continue

                media_url = clip.get("playbacks", [{}])[-1].get("url", "")
                print(f"⚾ {desc}\n🎥 {media_url}")

                # Generate trivia
                question = generate_trivia_question(desc)
                print("🧠 Trivia Question:")
                print(question)
                print("-" * 60 + "\n")

        except Exception as e:
            print(f"⚠️ Could not fetch content for game {game_id}: {e}")

if __name__ == "__main__":
    main()

