
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from data_sources.screener import ScreenerDataSource


def main():
    print("=" * 45)
    print("RupAI Screener.in Fundamentals Test")
    print("=" * 45)

    screener = ScreenerDataSource()

    try:
        result = screener.get_company_data("RELIANCE")

        print("\nSource:", result["source"])
        print("Symbol:", result["symbol"])
        print("Status:", result["status"])
        print("Ratios extracted:", result["ratios_extracted"])

        print("\n--- Fundamental Data ---")
        for name, value in result["fundamentals"].items():
            print(f"{name}: {value}")

        if result["ratios_extracted"] > 0:
            print("\nSUCCESS: Fundamental ratios extracted.")
        else:
            print("\nWARNING: No ratios extracted.")

    except Exception as error:
        print("\nTEST FAILED")
        print("Error:", repr(error))
        raise


if __name__ == "__main__":
    main()
