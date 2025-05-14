from fetch_play_by_play import get_game_play_by_play
from fetch_player_stats import fetch_player_stats
from fetch_play_by_play import generate_trivia_from_play

def generate_trivia_for_game(game_pk):
    play_by_play_data = get_game_play_by_play(game_pk)
    
    trivia_questions = []
    for play in play_by_play_data['plays']:
        trivia = generate_trivia_from_play(play)
        if trivia:
            trivia_questions.append(trivia)
    
    return trivia_questions

# Test with a valid gamePk
game_pk = "xyz123"  # Replace with actual gamePk
trivia_questions = generate_trivia_for_game(game_pk)

for q in trivia_questions:
    print(f"Question: {q['question']}")
    print(f"Answer: {q['answer']}")

