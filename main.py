import os
import requests

from data_collector import collect_market_data


def send_telegram(message):
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    response = requests.post(
        url,
        json={
            "chat_id": chat_id,
            "text": message
        },
        timeout=20
    )

    print("Telegram status:", response.status_code)
    print("Telegram response:", response.text)

    response.raise_for_status()


def main():
    print("================================")
    print("RupAI Market Pipeline Diagnostic")
    print("================================")

    print("\nSTEP 1: Collecting market data...")

    try:
        market_data = collect_market_data()

        print("\nSTEP 2: Collector finished.")
        print("Data type:", type(market_data))
        print("Data received:", market_data)

    except Exception as error:
        print("\n❌ MARKET DATA ERROR")
        print("Error:", repr(error))

        send_telegram(
            "❌ RupAI Market Data Error\n\n"
            f"{repr(error)}"
        )

        return

    if not market_data:
        print("\n❌ Market data is empty.")

        send_telegram(
            "⚠️ RupAI Market Data\n\n"
            "Market API connected, but no data was returned."
        )

        return

    print("\nSTEP 3: Sending data to Telegram...")

    message = (
        "📊 RupAI Market Data Diagnostic\n\n"
        "Market data collection: ✅\n"
        "Telegram connection: Testing...\n\n"
        f"Data type: {type(market_data).__name__}\n\n"
        f"Data:\n{str(market_data)[:3000]}"
    )

    try:
        send_telegram(message)
        print("\n✅ COMPLETE PIPELINE SUCCESS")

    except Exception as error:
        print("\n❌ TELEGRAM ERROR")
        print("Error:", repr(error))


if __name__ == "__main__":
    main()
