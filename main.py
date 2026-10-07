import os
import requests

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

message = "✅ RupAI Market Intelligence is online!\n\nGitHub → Python → Telegram connection successful."

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

response = requests.post(
    url,
    json={
        "chat_id": CHAT_ID,
        "text": message
    }
)

response.raise_for_status()

print("Telegram message sent successfully!")
