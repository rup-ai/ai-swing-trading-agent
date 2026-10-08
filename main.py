from data_collector import collect_market_data
from alerts.telegram import TelegramAlert


def main():
    print("🚀 Starting RupAI Market Intelligence...")

    # 1. Collect market data
    market_data = collect_market_data()

    if not market_data:
        print("❌ No market data received.")
        return

    print("✅ Market data received.")

    # 2. Create Telegram alert service
    telegram = TelegramAlert()

    # 3. Prepare message
    message = (
        "📊 RupAI Market Data Report\n\n"
        "Market data collection successful! ✅\n\n"
        f"{str(market_data)[:3500]}"
    )

    # 4. Send to Telegram
    telegram.send_message(message)

    print("✅ Market data sent to Telegram.")


if __name__ == "__main__":
    main()
