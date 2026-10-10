
import os
import requests


class TelegramAlert:
    """Telegram notification service for RupAI."""

    MAX_MESSAGE_LENGTH = 3500

    def __init__(self):
        self.bot_token = os.environ["TELEGRAM_BOT_TOKEN"]
        self.chat_id = os.environ["TELEGRAM_CHAT_ID"]

        self.base_url = (
            f"https://api.telegram.org/bot{self.bot_token}"
        )

    def _split_message(self, message):
        """Split long reports without discarding their contents."""

        message = str(message)
        chunks = []
        current = ""

        for line in message.splitlines(keepends=True):
            while len(line) > self.MAX_MESSAGE_LENGTH:
                available = self.MAX_MESSAGE_LENGTH - len(current)

                if available > 0:
                    current += line[:available]
                    line = line[available:]

                if current:
                    chunks.append(current)
                    current = ""

            if len(current) + len(line) > self.MAX_MESSAGE_LENGTH:
                if current:
                    chunks.append(current)
                current = line
            else:
                current += line

        if current:
            chunks.append(current)

        return chunks or [""]

    def send_message(self, message):
        """Send one or more Telegram messages and verify delivery."""

        chunks = self._split_message(message)
        results = []

        for index, chunk in enumerate(chunks, start=1):
            response = requests.post(
                f"{self.base_url}/sendMessage",
                json={
                    "chat_id": self.chat_id,
                    "text": chunk
                },
                timeout=20
            )

            response.raise_for_status()

            try:
                payload = response.json()
            except ValueError as error:
                raise RuntimeError(
                    "Telegram returned an invalid JSON response."
                ) from error

            if not payload.get("ok"):
                raise RuntimeError(
                    f"Telegram rejected message {index}: {payload}"
                )

            results.append(payload)

            print(
                f"Telegram message {index}/{len(chunks)} sent successfully."
            )

        return results
