from data_collector import collect_market_data
from alerts.telegram import TelegramAlert


def format_market_report(data):
    """
    Convert collected market data into a Telegram-friendly report.
    """

    message = "📊 RupAI Market Data Test\n\n"

    if isinstance(data, dict):
        message += f"Data received: ✅\n\n"
        message += str(data)[:3500]
    else:
        message += "Data received: ✅\n\n"
        message += str(data)[:3500]

    return message


def main():
    print("Starting RupAI Market Intelligence...")

    # Collect market data
    market_data = collect_market_data()

    if not market_data:
        print("❌ No market data received.")
        return

    print("✅ Market data received.")

    # Create Telegram alert service
    telegram = TelegramAlert()

    # Format report
    report = format_market_report(market_data)

    # Send report
    telegram.send_message(report)

    print("✅ Market report sent to Telegram.")


if __name__ == "__main__":
    main()
