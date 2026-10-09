
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from data_sources.screener import ScreenerDataSource
from alerts.telegram import TelegramAlert


def main():
    print("Fetching Screener.in fundamentals...")

    screener = ScreenerDataSource()
    result = screener.get_company_data("RELIANCE")

    fundamentals = result["fundamentals"]

    message_lines = [
        "RupAI Market Intelligence",
        "",
        "SCREENER.IN FUNDAMENTALS",
        f"Stock: {result['symbol']}",
        f"Status: {result['status']}",
        "",
    ]

    for key, value in fundamentals.items():
        display_name = key.replace("_", " ").title()
        message_lines.append(f"{display_name}: {value or 'Not available'}")

    message_lines.extend([
        "",
        f"Ratios extracted: {result['ratios_extracted']}",
        "",
        "Note: Fundamental data only. Not a buy/sell recommendation."
    ])

    message = "\n".join(message_lines)

    print("Sending report to Telegram...")

    telegram = TelegramAlert()
    telegram.send_message(message)

    print("Telegram report sent successfully.")


if __name__ == "__main__":
    main()
