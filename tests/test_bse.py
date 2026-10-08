import sys
from pathlib import Path

# Add project root to Python path
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from data_sources.bse import BSEDataSource


def main():

    print("================================")
    print("RupAI BSE Connector Test")
    print("================================")

    bse = BSEDataSource()

    # RELIANCE BSE scrip code
    scrip_code = "500325"

    print(
        f"\nTesting BSE scrip: {scrip_code}"
    )

    try:

        data = bse.get_stock_data(
            scrip_code
        )

        print(
            "\n✅ BSE market request successful."
        )

        print("Source:", bse.name)
        print(
            "Scrip Code:",
            scrip_code
        )

        print("\nResponse received:")
        print(
            str(data)[:3000]
        )

    except Exception as error:

        print(
            "\n❌ BSE request failed."
        )

        print(
            "Error:",
            repr(error)
        )


if __name__ == "__main__":
    main()
