
from providers.market_api import MarketDataSource
from providers.data_normalizer import MarketDataNormalizer
from analysis.stock_analyzer import analyze_stock


def main():
    symbol = "RELIANCE"

    print("Testing complete stock analysis pipeline:", symbol)

    api = MarketDataSource()
    normalizer = MarketDataNormalizer()

    raw_data = api.get_stock(symbol, exchange="NSE")

    normalized = normalizer.normalize(
        symbol=symbol,
        historical_data=raw_data
    )

    result = analyze_stock(normalized)

    print("\nAnalysis result:")
    print(result)

    assert result["symbol"] == symbol
    assert result["status"] == "SUCCESS", result

    indicators = result["indicators"]
    analysis = result["analysis"]

    assert indicators["latest_close"] > 0
    assert indicators["rsi_14"] is not None
    assert analysis["trend"] in {
        "UPTREND",
        "DOWNTREND",
        "MIXED",
        "INSUFFICIENT_HISTORY",
        "INSUFFICIENT_DATA",
    }

    print("\nPASS: Stock analysis pipeline completed.")


if __name__ == "__main__":
    main()
