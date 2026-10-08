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

        url = f"{self.base_url}/sendMessage"

        response = requests.post(
            url,
            json={
                "chat_id": self.chat_id,
                "text": message
            },
            timeout=20
        )

        response.raise_for_status()

        return response.json()
