import requests

# Fetch the play-by-play data for a given game
def get_game_play_by_play(game_pk):
    url = f"https://statsapi.mlb.com/api/v1/game/{game_pk}/playByPlay"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching play-by-play for game {game_pk}: {response.status_code}")
        return None

# Detect the event type based on the play description
def detect_event_from_play(play):
    description = play['result']['description'].lower()

    if 'home run' in description:
        return 'home_run'
    elif 'hit' in description:
        return 'hit'
    elif 'steals' in description:
        return 'steal'
    elif 'strikeout' in description:
        return 'strikeout'
    elif 'fans' in description or 'strikes out' in description:
        return 'strikeout'
    else:
        return None

# Example usage
if __name__ == "__main__":
    game_pk = "xyz123"  # Replace with actual gamePk
    play_by_play_data = get_game_play_by_play(game_pk)
    
    if play_by_play_data:
        trivia_questions = []
        for play in play_by_play_data['plays']:
            trivia = generate_trivia_from_play(play)
            if trivia:
                trivia_questions.append(trivia)
        
        # Print trivia questions
        for q in trivia_questions:
            print(f"Question: {q['question']}")
            print(f"Answer: {q['answer']}")

