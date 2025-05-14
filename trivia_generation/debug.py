import json
import statsapi

# Load highlights
with open("highlight_data.json") as f:
    highlights = json.load(f)

print(f"\n\U0001F3AF Loaded {len(highlights)} highlights\n")

def extract_player_ids(keywords):
    return [kw["value"] for kw in keywords if kw.get("type") in ["player", "player_id"] and kw["value"].isdigit()]

def extract_stat_field(title):
    keyword_map = {
        "home run": "homeRuns",
        "double": "doubles",
        "triple": "triples",
        "rbi": "rbi",
        "walk": "baseOnBalls",
        "steal": "stolenBases",
        "strikeout": "strikeOuts",
        "hit": "hits"
    }
    title_lower = title.lower()
    for keyword, stat in keyword_map.items():
        if keyword in title_lower:
            return stat
    return None

def get_stat_from_data(player_data, stat_field, scope="season"):
    stats_list = player_data.get("stats", [])
    for entry in stats_list:
        if scope in entry.get("type", {}).get("displayName", "").lower():
            splits = entry.get("splits", [])
            if splits and isinstance(splits, list):
                stat_dict = splits[0].get("stat", {})
                return stat_dict.get(stat_field)
    return None

def debug_player(player_id):
    try:
        player_id_str = str(player_id)
        season_data = statsapi.player_stat_data(player_id_str, group="hitting", type="season")
        career_data = statsapi.player_stat_data(player_id_str, group="hitting", type="career")

        print(f"\n\U0001F50D Player ID: {player_id_str}")

        for label, data in [("Season", season_data), ("Career", career_data)]:
            print(f"\n\U0001F4E6 {label} Data:")
            print(f"  - Type: {type(data)}")
            print(f"  - Keys: {list(data.keys())}")
            print(f"  - 'stats' type: {type(data.get('stats'))}")

    except Exception as e:
        print(f"\n\u274C Error fetching player {player_id}: {e}")

# Main loop
for highlight in highlights:
    title = highlight.get("title", "")
    keywords = highlight.get("keywords", [])
    stat_field = extract_stat_field(title)
    player_ids = extract_player_ids(keywords)

    print(f"\U0001F50D Title: {title}")
    print(f"   → matched stat_field: {stat_field}")

    if not player_ids or not stat_field:
        print("   ⚠️ Skipping: missing player or no stat keyword")
        continue

    for player_id in player_ids:
        debug_player(player_id)
