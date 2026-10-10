
from providers.market_api import MarketDataSource
from analysis.market_scanner import scan_market


def main():
    symbol = "RELIANCE"

    print("Testing market scanner with real API data:", symbol)

    api = MarketDataSource()
    raw_data = api.get_stock(symbol, exchange="NSE")

    result = scan_market({
        symbol: raw_data
    })

    print("\nScanner summary:")
    print("Scanned:", result["scanned"])
    print("Analyzed:", result["analyzed"])
    print("Failed:", result["failed"])

    print("\nRanked stocks:")
    for stock in result["ranked_stocks"]:
        print(stock)

    if result["analyzed"] != 1:
        print("\nFailures:", result["failures"])

    assert result["scanned"] == 1
    assert result["analyzed"] == 1, result["failures"]
    assert len(result["ranked_stocks"]) == 1
    assert result["ranked_stocks"][0]["symbol"] == symbol
    assert result["ranked_stocks"][0]["score"] is not None

    print("\nPASS: Market scanner integration test completed.")


if __name__ == "__main__":
    main()
