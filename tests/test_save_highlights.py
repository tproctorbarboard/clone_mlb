import requests
import json

def get_highlights(game_id):
    url = f"https://statsapi.mlb.com/api/v1/game/{game_id}/content"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"❌ Failed to fetch highlights (status code {response.status_code})")
        return []
    data = response.json()
    highlights = data.get('highlights', {}).get('highlights', {}).get('items', [])
    return highlights

def extract_player_ids(keywords):
    player_ids = []
    for keyword in keywords:
        if keyword.get('type') == 'player_id':
            player_ids.append(keyword.get('value'))
    return player_ids

def main():
    game_id = 777960  # Replace with your desired game ID
    print(f"🔍 Getting highlights for game ID: {game_id}")
    highlights = get_highlights(game_id)
    print(f"🔍 Found {len(highlights)} highlight clips\n")
    enriched_clips = []

    for clip in highlights:
        title = clip.get('title', 'Untitled')
        keywords = clip.get('keywordsAll', [])
        player_ids = extract_player_ids(keywords)
        enriched_clips.append({
            'title': title,
            'player_ids': player_ids,
            'keywords': keywords
        })
        print(f"🎬 {title}")
        if player_ids:
            print(f"   🧍 Player IDs: {', '.join(player_ids)}")
        else:
            print("   ⚠️ No player IDs found.")
        print()

    with open("highlight_data.json", "w") as f:
        json.dump(enriched_clips, f, indent=2)
    print("💾 highlight_data.json saved.")

if __name__ == "__main__":
    main()

