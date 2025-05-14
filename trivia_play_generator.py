import requests
from fetch_player_stats import fetch_player_stats

def generate_trivia_from_play(play):
    player_name = play['matchup']['batter']['fullName']
    player_id = play['matchup']['batter']['id']
    event_type = play['result']['eventType']

    print(f"[DEBUG] Generating trivia for: {player_name} (ID: {player_id}), Event: {event_type}")
    stats = fetch_player_stats(player_id)
    print(f"[DEBUG] Stats for {player_name} (ID: {player_id}): {stats}")

    def warn_if_zero(val): return f"{val} ⚠️ (may not be updated)" if val == 0 else str(val)

    question = "No trivia question available for this event."
    answer = "N/A"

    if event_type == "caught_stealing_2b":
        answer = warn_if_zero(stats.get("caughtStealing", 0))
        question = f"{player_name} was caught stealing. How many times has he been caught stealing this season?"

    elif event_type == "double":
        answer = warn_if_zero(stats.get("doubles", 0))
        question = f"{player_name} hit a double. How many doubles has he hit this season?"

    elif event_type == "fielders_choice":
        answer = warn_if_zero(stats.get("runs", 0))
        question = f"{player_name} reached on a fielder's choice. How many runs has he scored this season?"

    elif event_type == "field_out":
        outs = stats.get("groundOuts", 0) + stats.get("airOuts", 0)
        answer = warn_if_zero(outs)
        question = f"{player_name} was retired. How many outs has he made this season?"

    elif event_type == "force_out":
        answer = warn_if_zero(stats.get("plateAppearances", 0))
        question = f"{player_name} was forced out. How many plate appearances does he have this season?"

    elif event_type == "grounded_into_double_play":
        answer = warn_if_zero(stats.get("groundIntoDoublePlay", 0))
        question = f"{player_name} grounded into a double play. How many double plays has he grounded into this season?"

    elif event_type == "hit_by_pitch":
        answer = warn_if_zero(stats.get("hitByPitch", 0))
        question = f"{player_name} was hit by a pitch. How many times has he been hit this season?"

    elif event_type == "home_run":
        answer = warn_if_zero(stats.get("homeRuns", 0))
        question = f"{player_name} hit a home run. How many home runs does he have this season?"

    elif event_type == "sac_fly":
        answer = warn_if_zero(stats.get("sacFlies", 0))
        question = f"{player_name} hit a sacrifice fly. How many sac flies has he hit this season?"

    elif event_type == "single":
        hits = stats.get("hits", 0)
        doubles = stats.get("doubles", 0)
        triples = stats.get("triples", 0)
        homers = stats.get("homeRuns", 0)
        singles = hits - doubles - triples - homers
        answer = warn_if_zero(singles)
        question = f"{player_name} hit a single. How many singles has he hit this season?"

    elif event_type == "strikeout":
        answer = warn_if_zero(stats.get("strikeOuts", 0))
        question = f"{player_name} struck out. How many strikeouts does he have this season?"

    elif event_type == "walk":
        answer = warn_if_zero(stats.get("baseOnBalls", 0))
        question = f"{player_name} drew a walk. How many walks has he drawn this season?"

    if player_name == "Nick Gonzales":
        print(f"[MATCHED TRIVIA] Question: {question}")
        print(f"[MATCHED TRIVIA] Event Type: {event_type}")
        print(f"[MATCHED TRIVIA] Full Play Description: {play['result'].get('description')}")

    return question, answer

