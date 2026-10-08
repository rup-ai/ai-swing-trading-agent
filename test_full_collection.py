from stock_universe import get_initial_universe
from data_collector import collect_market_data


def main():

    print("======================================")
    print("RupAI Market Data Collection Test")
    print("======================================")

    stocks = get_initial_universe()

    print(f"\nTotal universe: {len(stocks)} stocks")

    # First test with 10 stocks
    test_stocks = stocks[:10]

    print(f"\nTesting: {len(test_stocks)} stocks")

    print("\nStocks being tested:")

    for symbol in test_stocks:
        print("-", symbol)

    print("\nCollecting market data...")

    data = collect_market_data(test_stocks)

    if not data:

        print("\n❌ NO DATA RETURNED")
        return

    successful = 0
    failed = 0

    print("\n======================================")
    print("RESULT")
    print("======================================")

    for symbol, result in data.items():

        if isinstance(result, dict) and "error" in result:

            failed += 1
            print(f"❌ {symbol} → {result['error']}")

        else:

            successful += 1
            print(f"✅ {symbol}")

    print("\nStocks requested:", len(test_stocks))
    print("Successful:", successful)
    print("Failed:", failed)

    if successful > 0:

        print("\n🎉 MARKET DATA COLLECTION WORKING")

    else:

        print("\n❌ NO STOCK DATA RECEIVED")


if __name__ == "__main__":
    main()
