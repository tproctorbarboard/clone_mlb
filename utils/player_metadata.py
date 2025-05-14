### utils/player_metadata.py
import statsapi

def get_player_metadata(player_name):
    try:
        player_info = statsapi.lookup_player(player_name)
        if not player_info:
            print(f"⚠️ Could not find player info for: {player_name}")
            return None

        player = player_info[0]
        player_id = player['id']
        debut = player.get("mlb_debut", "Unknown")
        team = player.get("current_team", "Unknown")

        # Pull season stats for extra validation
        stats_data = statsapi.player_stat_data(player_id, group="hitting", type="season")
        stats_2025 = next((s for s in stats_data.get("stats", []) if s["season"] == "2025"), None)
        homers = stats_2025["stats"].get("homeRuns", "?") if stats_2025 else "?"

        return {
            "name": player_name,
            "debut": debut,
            "team": team,
            "home_runs": homers
        }

    except Exception as e:
        print(f"⚠️ Error in statsapi lookup for {player_name}: {e}")
        return None


### run.py
from data_ingestion.significant_event_Watcher import get_significant_events
from trivia_generation.generate_questions import generate_trivia_question
from utils.player_metadata import get_player_metadata
import statsapi

def main():
    print("MLB Trivia Generator started...")
    print("Checking for home run events...\n")

    try:
        events = get_significant_events()

        for event in events:
            desc = event["description"]
            context = event.get("game_context", "")
            earlier = event.get("earlier_plays", "")
            prior_hr_count = event.get("home_runs_before_this", 0)
            game_id = event.get("game_id")

            if not game_id or not isinstance(game_id, int):
                print(f"⚠️ Skipping event with invalid game ID: {game_id}")
                continue
            if 600000 <= game_id < 700000:
                print(f"⚠️ Skipping Spring Training game ID: {game_id}")
                continue

            try:
                boxscore = statsapi.boxscore_data(game_id)

                if "teams" not in boxscore and "teamInfo" in boxscore:
                    boxscore["teams"] = {
                        "home": {"team": boxscore["teamInfo"]["home"]},
                        "away": {"team": boxscore["teamInfo"]["away"]},
                    }

                if "teams" not in boxscore:
                    print(f"⚠️ Raw boxscore missing 'teams' key for game {game_id}:\n{boxscore}")
                    raise KeyError("Missing 'teams' key in boxscore")

                home = boxscore['teams']['home']
                away = boxscore['teams']['away']

                home_team_name = home['team']['teamName']
                away_team_name = away['team']['teamName']
                home_hits = home.get('teamStats', {}).get('batting', {}).get('hits', '?')
                away_hits = away.get('teamStats', {}).get('batting', {}).get('hits', '?')

                team_stats = f"{home_team_name} Hits: {home_hits}, {away_team_name} Hits: {away_hits}"
            except Exception as e:
                print(f"⚠️ Failed to pull boxscore: {e}")
                team_stats = "Team stats unavailable"

            player_name = desc.split(" homers")[0].strip()

            player_info = get_player_metadata(player_name)
            debut = player_info["debut"] if player_info else "Unknown"
            team = player_info["team"] if player_info else "Unknown"
            hr_count = player_info["home_runs"] if player_info else "?"

            full_input = (
                f"Factual context:\n"
                f"- Player: {player_name}\n"
                f"- MLB Debut: {debut}\n"
                f"- Current Team: {team}\n"
                f"- Season HRs: {hr_count}\n"
                f"- Game: {context}\n"
                f"- Earlier plays: {earlier}\n"
                f"- Home runs before this: {prior_hr_count}\n"
                f"- Team boxscore: {team_stats}\n\n"
                f"Event: {desc}"
            )

            question = generate_trivia_question(full_input)
            print("🧠 Trivia Question:")
            print(question)
            print("-" * 60 + "\n")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()

