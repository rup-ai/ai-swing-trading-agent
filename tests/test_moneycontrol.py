
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from data_sources.moneycontrol import MoneycontrolDataSource


def main():
    print("=" * 45)
    print("RupAI Moneycontrol Connector Test")
    print("=" * 45)

    source = MoneycontrolDataSource()

    # Public Moneycontrol market page
    url = "https://www.moneycontrol.com/markets/"

    try:
        result = source.get_page_data(url)

        print("\nSource:", result["source"])
        print("Status:", result["status"])
        print("Page title:", result["title"])
        print("HTML content length:", result["content_length"])
        print("\nPage preview:")
        print(result["page_text_preview"])
        print("\nNote:", result["note"])

        print("\nSUCCESS: Moneycontrol page fetched.")

    except Exception as error:
        print("\nTEST FAILED")
        print("Error:", repr(error))
        raise


if __name__ == "__main__":
    main()
