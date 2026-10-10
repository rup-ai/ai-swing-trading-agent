
from unittest.mock import patch
import main


def main_test():
    sample_market_data = {
        "RELIANCE": {
            "data": [
                {
                    "date": f"2026-09-{day:02d}",
                    "open": 100 + day,
                    "high": 102 + day,
                    "low": 99 + day,
                    "close": 101 + day,
                    "volume": 100000,
                    "turnover": 10100000
                }
                for day in range(1, 21)
            ]
        }
    }

    with patch(
        "main.collect_market_data",
        return_value=sample_market_data
    ), patch(
        "main.scan_market",
        return_value={
            "scanned": 1,
            "analyzed": 1,
            "failed": 0,
            "ranked_stocks": [
                {
                    "rank": 1,
                    "symbol": "RELIANCE",
                    "score": 75,
                    "rating": "HIGHER_RANKED",
                    "reasons": ["Test ranking."]
                }
            ],
            "failures": []
        }
    ), patch(
        "main.format_ranked_report",
        return_value="RUPAI TEST REPORT"
    ), patch(
        "main.TelegramAlert"
    ) as telegram_class:

        main.main()

        telegram_class.return_value.send_message.assert_called_once_with(
            "RUPAI TEST REPORT"
        )

    print("\nPASS: Main pipeline sends the ranked report.")


if __name__ == "__main__":
    main_test()
