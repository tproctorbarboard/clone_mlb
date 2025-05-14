import json
import requests

SEASON = "2025"
HIGHLIGHT_FILE = "highlight_data.json"

def get_player_stats(player_id, season):
    url = f"https://statsapi.mlb.com/api/v1/people/{player_id}/stats?stats=season&season={season}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"  ⚠️ Failed to fetch stats for player {player_id} (HTTP {response.status_code})")
        return None
    data = response.json()
    try:
        splits = data["stats"][0]["splits"]
        if not splits:
            return None
        return splits[0]["stat"]
    except (KeyError, IndexError, TypeError):
        return None

def main():
    try:
        with open(HIGHLIGHT_FILE, "r") as f:
            highlights = json.load(f)
    except FileNotFoundError:
        print(f"❌ Highlight file {HIGHLIGHT_FILE} not found.")
        return

    print(f"🎞️ Found {len(highlights)} highlight clips\n")

    for clip in highlights:
        title = clip.get("title", "Untitled")
        print(f"🎬 {title}")

        player_ids = clip.get("player_ids", [])
        if not player_ids:
            print("   ⚠️ No player IDs found.\n")
            continue

        for pid in player_ids:
            stats = get_player_stats(pid, SEASON)
            if stats:
                print(f"   🧍 Player ID {pid} Stats:")
                print(f"      AVG: {stats.get('avg', 'N/A')} | HR: {stats.get('homeRuns', 'N/A')} | RBI: {stats.get('rbi', 'N/A')}")
            else:
                print(f"   ⚠️ No season stats available for Player ID {pid}")
        print()

if __name__ == "__main__":
    main()

