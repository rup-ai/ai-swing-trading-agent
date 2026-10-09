
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from data_sources.moneycontrol import MoneycontrolDataSource


def main():
    source = MoneycontrolDataSource()

    print("=" * 45)
    print("RupAI Moneycontrol Data Extraction Test")
    print("=" * 45)

    result = source.get_stock_data()

    print("Source:", result["source"])
    print("Status:", result["status"])
    print("Company:", result["title"])
    print("Metrics extracted:", result["metrics_extracted"])

    print("\n--- Market Data ---")
    for key, value in result["fundamentals"].items():
        print(f"{key}: {value if value is not None else 'Not found'}")

    if result["metrics_extracted"] == 0:
        print("\nWARNING: No metrics found.")
        print("Page preview:")
        print(result["page_text_preview"])
    else:
        print("\nExtraction returned data.")
        print("Note:", result["note"])


if __name__ == "__main__":
    main()
