
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from data_sources.moneycontrol import MoneycontrolDataSource


def main():
    source = MoneycontrolDataSource()

    try:
        url = source.RELIANCE_URL
        html = source.get_page(url)

        print("HTTP request successful")
        print("URL:", url)
        print("HTML length:", len(html))
        print("\n--- HTML preview (first 2500 characters) ---")
        print(html[:2500])

        text = source._clean_text(html)

        print("\n--- Page text preview (first 2500 characters) ---")
        print(text[:2500])

        result = source.get_stock_data(url)
        print("\nMetrics extracted:", result["metrics_extracted"])
        print(result["fundamentals"])

    except Exception as error:
        print("\nDEBUG TEST ERROR:", repr(error))
        raise


if __name__ == "__main__":
    main()
