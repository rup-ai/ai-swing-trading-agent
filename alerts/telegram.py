import os
import requests


class TelegramAlert:
    """
    Telegram notification service for RupAI Market Intelligence.
    """

    def __init__(self):
        self.bot_token = os.environ["TELEGRAM_BOT_TOKEN"]
        self.chat_id = os.environ["TELEGRAM_CHAT_ID"]

        self.base_url = (
            f"https://api.telegram.org/bot{self.bot_token}"
        )

    def send_message(self, message):
        """
        Send a text message to Telegram.
        """

        # Telegram text message limit is 4096 characters.
        # Keep a safe limit for our market reports.
        message = str(message)[:3000]

        url = f"{self.base_url}/sendMessage"

        response = requests.post(
            url,
            json={
                "chat_id": self.chat_id,
                "text": message
            },
            timeout=20
        )

        print("Telegram HTTP status:", response.status_code)
        print("Telegram API response:", response.text)

        if response.status_code != 200:
            raise RuntimeError(
                f"Telegram API error: {response.text}"
            )

        return response.json()
