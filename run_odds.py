from odds.game_selector import get_snb_game
from odds.prediction_manager import submit_prediction, load_predictions
from odds.live_tracker import get_game_stats
from odds.results_evaluator import evaluate_winners

# Select SNB Game
game = get_snb_game()
print(f"\nSunday Night Baseball: {game['away_team']} @ {game['home_team']} (gamePk: {game['gamePk']})\n")

# Submit a sample user guess
submit_prediction(game['gamePk'], "jonathan", {
    "strikeouts": 8,
    "home_runs": 3
})

# Get current game stats (live)
stats = get_game_stats(game['gamePk'])
print(f"Live Stats: {stats}")

# Load predictions
preds = load_predictions(game['gamePk'])

# Evaluate winner
ranked = evaluate_winners(preds, stats)
print(f"\nLeaderboard:\n{ranked}")

