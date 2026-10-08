from stock_universe import get_initial_universe


def main():
    print("====================================")
    print("RupAI Stock Universe Test")
    print("====================================")

    stocks = get_initial_universe()

    print("\nTotal stocks found:", len(stocks))

    print("\nFirst 20 stocks:")

    for i, symbol in enumerate(stocks[:20], start=1):
        print(f"{i}. {symbol}")

    if len(stocks) >= 400:
        print("\n✅ SUCCESS")
        print("NIFTY 500 universe loaded successfully.")

    else:
        print("\n⚠️ WARNING")
        print("Universe contains fewer than 400 stocks.")


if __name__ == "__main__":
    main()
