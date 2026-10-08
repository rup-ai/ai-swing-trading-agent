import sys
from pathlib import Path

# Add project root to Python path
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from data_sources.chartink import ChartinkDataSource


def main():

    print("================================")
    print("RupAI Chartink Connector Test")
    print("================================")

    chartink = ChartinkDataSource()

    # Public Chartink page for connection testing
    scan_url = "https://chartink.com/"

    print(
        f"\nTesting URL: {scan_url}"
    )

    try:

        result = chartink.get_scan_results(
            scan_url
        )

        print(
            "\n✅ Chartink request successful."
        )

        print("Source:", result["source"])
        print("Status:", result["status"])
        print(
            "Content length:",
            result["content_length"]
        )

    except Exception as error:

        print(
            "\n❌ Chartink request failed."
        )

        print(
            "Error:",
            repr(error)
        )


if __name__ == "__main__":
    main()
