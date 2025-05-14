import statsapi

game_id = 747471  # Replace with one that breaks if needed

try:
    boxscore = statsapi.boxscore_data(game_id)
    print("\n✅ Successfully pulled boxscore.")
    print("📦 Top-level keys in boxscore:", list(boxscore.keys()))
    if "teamInfo" in boxscore:
        print("\nℹ️ teamInfo contents:", boxscore["teamInfo"])
    if "teams" in boxscore:
        print("\n📦 teams contents:", boxscore["teams"])
except Exception as e:
    print(f"❌ Error: {e}")
    
    # Now, directly hit the underlying API URL manually
    import requests
    r = requests.get(f"https://statsapi.mlb.com/api/v1/game/{game_id}/boxscore")
    print("📥 Raw response keys:", list(r.json().keys()))
    print("📥 Raw gameData if present:", r.json().get("gameData", {}))

