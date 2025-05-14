import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load your API key from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Initialize model
model = genai.GenerativeModel("gemini-2.0-flash-lite")

def format_prompt(question, correct_answer):
    return f"""
You're generating trivia questions based on a reent MLB play; about mlb statistics. Your goal is to be concise, engaging, and to the point, like classic bar trivia. Think about the action, and keep the question sharp. Avoid repeating the same openers, no long introductions — just straightforward questions that fit into a live-game broadcast. The trivia should focus on the play and the relevant stats in a way that feels natural and conversational. 

Examples:
- "After that strikeout in the 4th inning, Mike Trout has how many K's on the season?"
- "With that double from Tyler O'Neill, how many doubles has he hit this year?"

No intros, no “paying attention” references. Just classic, no-frills trivia that gets to the point.
Less cheesy,just hey that was a great play by that player, how many times have they done that play this season, etc.

but mix them up dont repeat the same formats, ensure that there is logical flow and progression from the wind up and the question itself. keep it concise.

You’ll be given:
- A trivia question and the correct answer about a recent MLB play.

Your job:
1. Write a **concise trivia question** based on the play.
2. **Do not invent the correct answer** — it’s already provided.
3. Create 3 plausible incorrect answers close to the true value.
4. Shuffle the answer options randomly.
5. Avoid overly repetitive language; keep it sharp and to the point.

---

**Trivia Question:**
{question}

**Correct Answer:**
{correct_answer}

---

Output format (do not change this format):

<Concise trivia question with announcer-style tone>

A) <wrong_answer_1>  
B) <wrong_answer_2>  
C) <correct_answer>  
D) <wrong_answer_3>  

Answer: <letter corresponding to correct answer>
"""

def generate_mcq(question, correct_answer):
    prompt = format_prompt(question, correct_answer)
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"[ERROR] Gemini API failed: {e}"

