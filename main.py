from data_collector import collect_market_data
from data_formatter import format_market_report
from alerts.telegram import TelegramAlert


def main():
    print("🚀 Starting RupAI Market Intelligence...")

    market_data = collect_market_data()

    if not market_data:
        print("❌ No market data received.")
        return

    print("✅ Market data received.")

    report = format_market_report(
        market_data,
        max_stocks=10
    )

    telegram = TelegramAlert()

    telegram.send_message(report)

    print("✅ Formatted market report sent to Telegram.")


if __name__ == "__main__":
    main()
