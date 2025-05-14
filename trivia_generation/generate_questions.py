from dotenv import load_dotenv
import os
import re
import google.generativeai as genai

# Load your API key from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel("models/gemini-2.0-flash-lite")

def clean_description(desc):
    """
    Reformat 'homers (3)' → 'homers (his 3rd HR of the season)'
    so Gemini doesn't misread it as 3rd HR of the game.
    """
    def replacer(match):
        num = int(match.group(1))
        if 10 <= num % 100 <= 20:
            suffix = f"{num}th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(num % 10, "th")
            suffix = f"{num}{suffix}"
        return f"homers (his {suffix} HR of the season)"

    return re.sub(r'homers \((\d+)\)', replacer, desc)

def generate_trivia_question(event_description, player_name=None, stat_category=None, stat_value=None):
    """
    Generate a trivia question using an event description and optionally include stat context.
    """
    event_description = clean_description(event_description)

    stat_line = ""
    if player_name and stat_category and stat_value:
        stat_line = f"\nStat Context: {player_name} has {stat_value} {stat_category}."

    prompt = f"""
You are a structured, accurate MLB trivia generator.

Given a real MLB game event and known stat context, create a **factual, multiple-choice trivia question** that connects the event to:
- a known player stat (season or career),
- or a notable milestone directly related to the stat value.

✅ Guidelines:
- Tie the trivia to **what just happened** in the game.
- Ask directly about the provided stat (e.g., stolen bases, home runs, etc.).
- Do **not** include the stat value in the question or options.
- **Never make up** facts or context beyond the stat and event.
- Write like a sharp in-game broadcaster quizzing fans.

📎 Context provided:
Event: {event_description}{stat_line}

Respond in this format:
Q: <question>
A. <option A>
B. <option B>
C. <option C>
D. <option D>
Answer: <correct letter>
"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating trivia: {e}"

