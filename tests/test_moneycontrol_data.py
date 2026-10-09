
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from data_sources.moneycontrol import MoneycontrolDataSource


def main():
    source = MoneycontrolDataSource()
    result = source.get_stock_data()

    print("Source:", result["source"])
    print("Status:", result["status"])
    print("Company:", result["title"])
    print("Metrics extracted:", result["metrics_extracted"])
    print("\n--- Extracted Metrics ---")

    for key, value in result["fundamentals"].items():
        print(f"{key}: {value if value is not None else 'Not found'}")

    print("\nNote:", result["note"])


if __name__ == "__main__":
    main()
