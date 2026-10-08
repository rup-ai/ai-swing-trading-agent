from data_sources.nse import NSEDataSource


def main():

    print("================================")
    print("RupAI NSE Connector Test")
    print("================================")

    nse = NSEDataSource()

    symbol = "RELIANCE"

    print(f"\nTesting stock: {symbol}")

    try:

        data = nse.get_stock_data(symbol)

        print("\n✅ NSE stock request successful.")
        print("Source:", nse.name)
        print("Symbol:", symbol)

        print("\nResponse received:")
        print(str(data)[:3000])

    except Exception as error:

        print("\n❌ NSE stock request failed.")
        print("Error:", repr(error))


if __name__ == "__main__":
    main()
