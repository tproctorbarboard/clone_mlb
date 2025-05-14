# odds/results_evaluator.py
def evaluate_winners(predictions, actual):
    results = {}
    for user, guess in predictions.items():
        diff = abs(guess.get("strikeouts", 0) - actual["strikeouts"]) \
             + abs(guess.get("home_runs", 0) - actual["home_runs"])
        results[user] = diff

    # Sort by smallest difference
    return sorted(results.items(), key=lambda x: x[1])

