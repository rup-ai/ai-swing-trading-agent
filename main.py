from data_collector import collect_market_data
from alerts.telegram import TelegramAlert


def main():
    print("🚀 Starting RupAI Market Intelligence...")

    # Collect market data
    market_data = collect_market_data()

    if not market_data:
        print("❌ No market data received.")
        return

    print("✅ Market data received.")

    # Create Telegram service
    telegram = TelegramAlert()

    # Build report
    message = "📊 RupAI MARKET DATA REPORT\n\n"
    message += "Market data collection successful! ✅\n\n"

    count = 0

    for symbol, data in market_data.items():

        if count >= 10:
            break

        message += f"📌 {symbol}\n"

        if isinstance(data, dict) and "error" in data:
            message += f"Error: {data['error']}\n\n"
        else:
            message += f"{str(data)[:500]}\n\n"

        count += 1

    # Send to Telegram
    telegram.send_message(message)

    print("✅ Market report sent to Telegram.")


if __name__ == "__main__":
    main()
