import requests
import os
from trivia_play_generator import generate_trivia_from_play
from generate_gemini_trivia import generate_mcq  # Import Gemini wrapper
from trivia_generation.classify_utils import classify_field_out

def fetch_play_by_play(game_pk):
    url = f"https://statsapi.mlb.com/api/v1/game/{game_pk}/playByPlay"
    response = requests.get(url)
    return response.json()

def generate_all_trivia(game_pk):
    game_data = fetch_play_by_play(game_pk)
    trivia = []

    for play in game_data.get("allPlays", []):
        try:
            batter_info = play.get("matchup", {}).get("batter", {})
            player_name = batter_info.get("fullName", "Unknown")
            player_id = batter_info.get("id", "Unknown")

            result = play.get("result", {})
            event = result.get("event")
            event_type = result.get("eventType")
            description = result.get("description", "")

            # Refine field_out
            if event_type == "field_out":
                refined_type = classify_field_out(description)
                print(f"[DEBUG] Reclassified field_out → {refined_type}")
                event_type = refined_type

            q, a = generate_trivia_from_play(play)
            if "No trivia" not in q:
                print(f"\n[PLAY DESCRIPTION] {description}")
                print(f"[TRIVIA EVENT TYPE] {event_type}")
                trivia.append((q, a))

        except Exception as e:
            print(f"[SKIPPED] {play.get('result', {}).get('event')}: {e}")

    return trivia

if __name__ == "__main__":
    game_pk = 777924  # Replace with desired 2025 gamePk
    trivia_items = generate_all_trivia(game_pk)

    for i, (q, a) in enumerate(trivia_items, 1):
        print(f"\nQ{i}: {q}")
        print(f"A{i}: {a}")

        print("\n[Gemini Multiple Choice Question]")
        try:
            mcq = generate_mcq(q, a)
            print(mcq)
        except Exception as e:
            print(f"[Gemini ERROR] Failed to generate MCQ: {e}")

