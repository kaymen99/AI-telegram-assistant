import os, requests
from datetime import datetime

SCOPES = [
    "https://www.googleapis.com/auth/calendar.events",
    'https://www.googleapis.com/auth/contacts',
    "https://www.googleapis.com/auth/contacts.readonly",
    'https://www.googleapis.com/auth/gmail.readonly'
]
            
def print_agent_output(output):
    for message in output["messages"]:
        message.pretty_print()

def send_telegram_message(text):
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}&amp;parse_mode=MarkdownV2"
    response = requests.get(url).json()
    if not response["ok"]:
        return "Failed to send message"

    return "Message sent successfully on Telegram"
            
def receive_telegram_message(after_timestamp):
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
