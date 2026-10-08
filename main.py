import os
import requests


def main():
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    message = (
        "🧪 RupAI Telegram Diagnostic Test\n\n"
        "GitHub Actions is running successfully.\n"
        "Telegram API connection is being tested."
    )

    response = requests.post(
        url,
        json={
            "chat_id": chat_id,
            "text": message
        },
        timeout=20
    )

    print("Telegram HTTP status:", response.status_code)
    print("Telegram API response:", response.text)

    response.raise_for_status()

    result = response.json()

    if result.get("ok") is True:
        print("✅ Telegram accepted the message.")
    else:
        print("❌ Telegram did not accept the message.")


if __name__ == "__main__":
    main()
