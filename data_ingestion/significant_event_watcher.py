import datetime
import random

def get_significant_events():
    """
    Simulates detecting significant MLB events.
    Replace with real statsapi logic later.
    """
    # Simulate a single event (would come from statsapi)
    fake_event = {
        "id": f"game1234_hr_{datetime.datetime.now().timestamp()}",
        "description": f"{random.choice(['Shohei Ohtani', 'Aaron Judge', 'Mookie Betts'])} hit a 450-foot home run"
    }

    return [fake_event]

