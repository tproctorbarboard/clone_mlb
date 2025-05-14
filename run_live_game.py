# run_live_game.py

import time
from odds.live_tracker import get_game_stats
from odds.prediction_manager import submit_prediction, load_predictions
from odds.results_evaluator import evaluate_winners

# Use today's test game instead of SNB
GAME_PK = 777924  # Twins vs Orioles

# --- Simulate pre-game user predictions (only do once) ---
submit_prediction(GAME_PK, "tim", {"strikeouts": 12, "home_runs": 3})
submit_prediction(GAME_PK, "sarah", {"strikeouts": 9, "home_runs": 2})
submit_prediction(GAME_PK, "mike", {"strikeouts": 5, "home_runs": 4})

print(f"\nTracking Game {GAME_PK} (Twins vs Orioles)\n")

# --- Live tracking loop ---
try:
    while True:
        stats = get_game_stats(GAME_PK)
        print(f"Live Stats: {stats}")

        preds = load_predictions(GAME_PK)
        leaderboard = evaluate_winners(preds, stats)

        print("\nLeaderboard:")
        for user, diff in leaderboard:
            guess = preds[user]
            print(f"{user:<10} | Guess: {guess}, Error: {diff}")

        print("-" * 40)
        time.sleep(120)  # Refresh every 2 minutes

except KeyboardInterrupt:
    print("\nLive tracking stopped.")

