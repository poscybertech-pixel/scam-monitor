import os
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")

url = f"https://api.telegram.org/bot{token}/sendMessage"

response = requests.post(
    url,
    data={
        "chat_id": chat_id,
        "text": "🚨 Scam Monitor Test Alert\n\nThe Telegram notification system is ready."
    },
    timeout=30
)

if response.ok:
    print("Telegram message sent successfully.")
else:
    print("Telegram request failed.")
    print(response.text)
