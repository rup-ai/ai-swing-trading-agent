import sys
from pathlib import Path

# Add project root to Python path
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from data_sources.chartink import ChartinkDataSource


def main():

    print("========================================")
    print("RupAI Chartink Scanner Test")
    print("========================================")

    chartink = ChartinkDataSource()

    scanner_url = (
        "https://chartink.com/"
        "screener/profit-jump-by-200"
    )

    print("\nScanner:")
    print(scanner_url)

    try:

        result = chartink.get_scan_results(
            scanner_url
        )

        print("\nSource:", result["source"])
        print("Status:", result["status"])
        print(
            "Stocks found:",
            result["count"]
        )

        print("\nMatched stocks:")

        if result["stocks"]:

            for symbol in result["stocks"]:
                print("✅", symbol)

        else:

            print(
                "⚠️ No symbols extracted."
            )

        if result["count"] > 0:

            print(
                "\n🎉 CHARTINK SCANNER "
                "RESULT TEST SUCCESSFUL"
            )

        else:

            print(
                "\n⚠️ Chartink page loaded, "
                "but scanner symbols were not "
                "found in the HTML."
            )

    except Exception as error:

        print(
            "\n❌ Chartink scanner test failed."
        )

        print(
            "Error:",
            repr(error)
        )


if __name__ == "__main__":
    main()
