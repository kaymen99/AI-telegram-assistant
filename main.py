import time
from dotenv import load_dotenv
from src.agents.manager_agent import invoke_telegram_assistant
from src.utils import receive_message

# Load .env variables
load_dotenv()

def monitor_bot(after_timestamp):
    while True:
        new_messages = receive_message(after_timestamp)
        if new_messages:
            for message in new_messages:
                sent_message = (f"Message: {message['text']}\n"
                                f"Current Date/time: {message['date']}")
                invoke_telegram_assistant(sent_message)
        after_timestamp = int(time.time())
        time.sleep(10)  # Sleep for 20 seconds before checking again
        

if __name__ == "__main__":
    print("Telegram Assistant Manager is running")
    initial_timestamp = int(time.time())
    monitor_bot(initial_timestamp)