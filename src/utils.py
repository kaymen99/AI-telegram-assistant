import os, requests
from datetime import datetime

SCOPES = [
    "https://www.googleapis.com/auth/calendar.events",
    'https://www.googleapis.com/auth/contacts',
    "https://www.googleapis.com/auth/contacts.readonly",
    'https://www.googleapis.com/auth/gmail.readonly'
]

def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()
            
def receive_message(after_timestamp):
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    response = requests.get(url).json()
    if not response["result"]:
        return []

    new_messages = []

    for update in response["result"]:
        if "message" in update:
            message = update["message"]
            if message["date"] > after_timestamp:
                new_messages.append({
                    "text": message["text"],
                    "date": datetime.fromtimestamp(message["date"]).strftime("%Y-%m-%d %H:%M")
                })

    return new_messages
