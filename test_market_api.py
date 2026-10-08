from providers.market_api import MarketDataSource


def main():
    print("================================")
    print("RupAI Market Data Provider Test")
    print("================================")

    market_api = MarketDataSource()

    symbols = [
        "RELIANCE",
        "TCS",
        "INFY",
        "HDFCBANK",
        "ICICIBANK"
    ]

    print(f"\nTesting {len(symbols)} stocks...")

    try:
        data = market_api.get_multiple_stocks(symbols)

        print("\n✅ Provider responded.\n")

        for symbol, result in data.items():
            print(f"\n--- {symbol} ---")
            print(result)

    except Exception as error:
        print("\n❌ Provider test failed.")
        print("Error:", repr(error))


if __name__ == "__main__":
    main()
