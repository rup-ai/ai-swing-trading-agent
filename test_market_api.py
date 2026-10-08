from providers.market_api import MarketDataSource


def main():
    print("🚀 Starting market API test...")

    market_api = MarketDataSource()

    symbols = [
        "RELIANCE",
        "TCS",
        "INFY",
        "HDFCBANK",
        "ICICIBANK"
    ]

    try:
        data = market_api.get_multiple_stocks(symbols)

        print("\n✅ Market API responded successfully.\n")
        print("===== MARKET DATA =====")
        print(data)

    except Exception as error:
        print("\n❌ Market API test failed.")
        print("Error:", error)


if __name__ == "__main__":
    main()
