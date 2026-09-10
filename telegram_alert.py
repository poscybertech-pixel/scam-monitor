import os
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    if not BOT_TOKEN or not CHAT_ID:
        print("Telegram credentials are not configured.")
        return False

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    response = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": message
        },
        timeout=30
    )

    if response.ok:
        print("Telegram message sent successfully.")
        return True

    print("Telegram request failed.")
    print(response.text)
    return False


if __name__ == "__main__":
    send_telegram_message(
        "Scam Monitor test alert\n\n"
        "The Telegram notification system is ready."
    )
