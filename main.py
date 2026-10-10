
from data_collector import collect_market_data
from analysis.market_scanner import scan_market
from analysis.report_formatter import format_ranked_report
from alerts.telegram import TelegramAlert


def main():
    print("Starting RupAI Market Intelligence...")

    market_data = collect_market_data()

    if not market_data:
        print("No market data received. Stopping.")
        return

    print(f"Received data for {len(market_data)} stocks.")

    scan_result = scan_market(market_data)

    print(
        f"Analysis complete. "
        f"Analyzed: {scan_result['analyzed']}, "
        f"Failed: {scan_result['failed']}"
    )

    report = format_ranked_report(
        scan_result,
        max_stocks=10
    )

    print("\n" + report)

    if scan_result["analyzed"] == 0:
        print("No stocks were successfully analyzed. Not sending report.")
        return

    telegram = TelegramAlert()
    telegram.send_message(report)

    print("Ranked market report sent to Telegram.")


if __name__ == "__main__":
    main()
