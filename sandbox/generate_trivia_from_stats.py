import requests
import json

# Function to fetch player data from the MLB API
def fetch_player_stats(player_id):
    url = f"https://statsapi.mlb.com/api/v1/people/{player_id}/stats?stats=season"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Failed to fetch data for player {player_id}")
        return None

# Function to generate trivia questions from player stats
def generate_trivia_question(player_data):
    if player_data is None:
        return []

    questions = []
    for player in player_data['stats']:
        player_name = player['player']['fullName']
        stats = player['splits'][0]['stat']

        # Example question generation
        if 'homeRuns' in stats:
            question = f"How many home runs did {player_name} hit in the 2025 season?"
            options = [str(stats['homeRuns'] - 1), str(stats['homeRuns']), str(stats['homeRuns'] + 1), str(stats['homeRuns'] + 2)]
            answer = str(stats['homeRuns'])
            questions.append({
                'question': question,
                'options': options,
                'answer': answer
            })

        if 'avg' in stats:
            question = f"What is {player_name}'s batting average in the 2025 season?"
            options = [str(round(float(stats['avg']) - 0.02, 3)), str(stats['avg']), str(round(float(stats['avg']) + 0.02, 3)), str(round(float(stats['avg']) + 0.05, 3))]
            answer = str(stats['avg'])
            questions.append({
                'question': question,
                'options': options,
                'answer': answer
            })

        if 'rbi' in stats:
            question = f"How many RBIs did {player_name} have in the 2025 season?"
            options = [str(stats['rbi'] - 3), str(stats['rbi']), str(stats['rbi'] + 3), str(stats['rbi'] + 5)]
            answer = str(stats['rbi'])
            questions.append({
                'question': question,
                'options': options,
                'answer': answer
            })

    return questions

# Main function to generate and save trivia questions
def generate_trivia():
    # Sample player ID for Gabriel Arias
    player_id = 672356
    player_data = fetch_player_stats(player_id)
    
    # Generate trivia questions
    trivia_questions = generate_trivia_question(player_data)
    
    # Print the questions
    if trivia_questions:
        with open("generated_trivia_questions.json", "w") as outfile:
            json.dump(trivia_questions, outfile, indent=4)
        print("✅ Trivia questions generated and saved to generated_trivia_questions.json")
    else:
        print("❌ No trivia questions generated.")

# Run the trivia generation
generate_trivia()

