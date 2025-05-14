from datetime import datetime, timedelta
import statsapi

def get_significant_events():
    # Only pull games from yesterday (or hardcode date if needed)
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    games = statsapi.schedule(start_date=yesterday, end_date=yesterday)

    events = []

    for game in games:
        if game['status'] == 'Final':
            game_id = game['game_id']
            try:
                summary = statsapi.game_scoring_play_data(game_id)
            except Exception as e:
                print(f"⚠️ Failed to fetch summary for game {game_id}: {e}")
                continue

            plays = summary.get("plays", [])
            home = summary.get("home", {}).get("teamName", "Home")
            away = summary.get("away", {}).get("teamName", "Away")

            for i, play in enumerate(plays):
                desc = play.get("result", {}).get("description", "")
                desc = " ".join(desc.split())  # Clean whitespace

                if "homers" in desc.lower():
                    # Count earlier home runs
                    earlier_plays = plays[:i]
                    earlier_hr_count = sum(
                        1 for p in earlier_plays
                        if "homers" in p.get("result", {}).get("description", "").lower()
                    )

                    # Include up to 3 previous plays for context
                    recent_plays = plays[max(0, i - 3):i]
                    earlier_descriptions = [
                        p.get("result", {}).get("description", "") for p in recent_plays
                    ]
                    earlier_context = " | ".join(earlier_descriptions)

                    events.append({
                        "id": f"{game_id}_hr_{i}",
                        "game_id": game_id,  # ✅ critical for boxscore fetch
                        "description": desc,
                        "game_context": f"Inning: {play.get('about', {}).get('halfInning', '?').title()} {play.get('about', {}).get('inning', '?')} | Game: {away} at {home}",
                        "earlier_plays": earlier_context,
                        "home_runs_before_this": earlier_hr_count
                    })

    return events

