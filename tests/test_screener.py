import sys
from pathlib import Path

# Add project root to Python path
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from data_sources.screener import ScreenerDataSource


def main():

    print("========================================")
    print("RupAI Screener.in Connector Test")
    print("========================================")

    screener = ScreenerDataSource()

    symbol = "RELIANCE"

    print(
        f"\nTesting company: {symbol}"
    )

    try:

        result = screener.get_company_data(
            symbol
        )

        print(
            "\n✅ Screener.in request successful."
        )

        print(
            "Source:",
            result["source"]
        )

        print(
            "Symbol:",
            result["symbol"]
        )

        print(
            "Status:",
            result["status"]
        )

        print(
            "Content length:",
            result["content_length"]
        )

    except Exception as error:

        print(
            "\n❌ Screener.in request failed."
        )

        print(
            "Error:",
            repr(error)
        )


if __name__ == "__main__":
    main()
