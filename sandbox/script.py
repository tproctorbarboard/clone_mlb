import requests

def fetch_player_data(player_id):
    url = f"https://statsapi.mlb.com/api/v1/people/{player_id}/stats?stats=season"
    response = requests.get(url)

    # Check if the response is successful
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Failed to fetch data for player {player_id}")
        return None

def generate_trivia_question(player_data):
    # Debug print statement to check the structure of player_data
    print("Debugging player data:")
    print(player_data)  # This will print the entire data returned for debugging

    try:
        # Extracting player name and other details
        player_name = player_data['stats'][0]['player']['fullName']  # Adjust based on structure
        team_name = player_data['stats'][0]['team']['name']  # Adjust based on structure
        season_stats = player_data['stats'][0]  # Assuming we are dealing with the first season's stats

        # Example of creating trivia question
        question = f"Which team does {player_name} play for?"
        correct_answer = team_name
        print(f"Question: {question}")
        print(f"Correct Answer: {correct_answer}")
        return question, correct_answer

    except KeyError as e:
        print(f"❌ Missing key in player data: {e}")
        return None, None

def generate_trivia():
    player_ids = [672356, 608070, 642547, 700932, 467793]  # Example player IDs
    all_questions = []

    for player_id in player_ids:
        player_data = fetch_player_data(player_id)
        if player_data:
            question, correct_answer = generate_trivia_question(player_data)
            if question and correct_answer:
                all_questions.append({
                    'question': question,
                    'correct_answer': correct_answer
                })

    # If trivia questions were generated, save or print them
    if all_questions:
        print("Trivia Questions Generated:")
        for idx, q in enumerate(all_questions, start=1):
            print(f"{idx}. {q['question']} | Correct Answer: {q['correct_answer']}")
    else:
        print("❌ No trivia questions generated.")

# Run the function to generate trivia
if __name__ == "__main__":
    generate_trivia()

