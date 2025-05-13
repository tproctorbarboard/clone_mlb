import time
from data_ingestion.significant_event_watcher import get_significant_events
from trivia_generation.generate_questions import generate_trivia_question

def main(poll_interval=120):
    print("MLB Trivia Generator started...")
    seen_events = set()  # avoid repeating questions

    while True:
        try:
            print("Checking for new events...")
            events = get_significant_events()

            for event in events:
                event_id = event.get("id")  # must be unique (e.g. game_id + player_id + event_type)
                if event_id not in seen_events:
                    seen_events.add(event_id)
                    description = event["description"]
                    print("Detected: {description}")

                    question = generate_trivia_question(description)
                    print("Trivia Question:")
                    print(question)
                    print("-" * 60)

                    # Optional: save to database here
                    # db.save_question(event_id, question)

        except Exception as e:
            print(f"Error: {e}")

        print(f"Waiting {poll_interval} seconds...\n")
        time.sleep(poll_interval)

if __name__ == "__main__":
    main()

