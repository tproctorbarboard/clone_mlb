# odds/game_selector.py
import statsapi
from datetime import datetime, timedelta

def get_snb_game():
    today = datetime.today()
    next_sunday = today + timedelta((6 - today.weekday()) % 7)
    date_str = next_sunday.strftime('%Y-%m-%d')
    
    schedule = statsapi.schedule(start_date=date_str, end_date=date_str)
    if not schedule:
        raise ValueError("No games found for next Sunday")

    snb_game = max(schedule, key=lambda x: x['game_datetime'])
    return {
        "gamePk": snb_game['game_id'],
        "date": date_str,
        "home_team": snb_game['home_name'],
        "away_team": snb_game['away_name']
    }

