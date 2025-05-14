import json
import requests

# Example player IDs and corresponding stat keywords
player_ids = ['672356', '608070', '642547', '700932', '467793']  # Replace with actual player IDs
stat_keywords = {
    '672356': 'doubles',  # Example: 'doubles' stat for Gabriel Arias
    '608070': 'stolenBases',  # Example: 'stolenBases' stat for José Ramírez
    '642547': 'strikeOuts',  # Example: 'strikeOuts' stat for Freddy Peralta
    '700932': 'rbi',  # Example: 'rbi' stat for Kyle Manzardo
    '467793': 'rbi',  # Example: 'rbi' stat for Carlos Santana
}

# Function to safely access the stat
def safe_get_stat(data, field):
    try:
        # Print the raw data for debugging
        print(f"🔍 Raw player data: {json.dumps(data, indent=2)}")
        return data["stats"][0]["splits"][0]["stat"].get(field)
    except (KeyError, IndexError, AttributeError) as e:
        print(f"❌ Error while accessing stats: {e}")
        return None

# Function to safely get player name
def safe_get_name(data):
    try:
        # Print the raw player data for debugging
        print(f"🔍 Raw player data: {json.dumps(data, indent=2)}")
        return f"{data['first_name']} {data['last_name']}"
    except KeyError as e:
        print(f"❌ Error while accessing player name: {e}")
        return None

# Function to fetch player season and career data (replace with actual API)
def fetch_player_data(player_id):
    # Example API endpoint (replace with actual)
    url = f"https://statsapi.mlb.com/api/v1/players/{player_id}/stats"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Failed to fetch data for player {player_id}")
        return None

# Main script to generate trivia questions
def generate_trivia():
    questions = []
    
    for player_id in player_ids:
        # Fetch player data (season and career)
        data = fetch_player_data(player_id)
        if data:
            # Extract player name
            player_name = safe_get_name(data)
            
            if player_name:
                print(f"📚 Player Name: {player_name}")
                
                # Lookup the stat for the player
                stat_field = stat_keywords.get(player_id)
                if stat_field:
                    stat_value = safe_get_stat(data, stat_field)
                    if stat_value:
                        question = f"How many {stat_field} does {player_name} have this season?"
                        print(f"✅ {question}")
                        questions.append({"question": question, "answer": stat_value})
                    else:
                        print(f"❌ Stat not found for player {player_name}")
                else:
                    print(f"❌ No stat keyword found for player {player_name}")
            else:
                print(f"❌ Missing player name for player ID: {player_id}")
        else:
            print(f"❌ No data found for player ID: {player_id}")
    
    # Save questions to a file
    with open("generated_trivia_questions.json", "w") as f:
        json.dump(questions, f, indent=2)
    
    if questions:
        print(f"✅ Saved {len(questions)} trivia questions to generated_trivia_questions.json")
    else:
        print("❌ No trivia questions generated.")

# Run the trivia generation
if __name__ == "__main__":
    generate_trivia()

