
from providers.market_api import MarketDataSource
from providers.data_normalizer import MarketDataNormalizer
from analysis.technical_indicators import calculate_indicators
from analysis.trend_analysis import analyze_trend


def main():
    symbol = "RELIANCE"

    print("Testing trend analysis with real data:", symbol)

    api = MarketDataSource()
    normalizer = MarketDataNormalizer()

    raw_data = api.get_stock(symbol, exchange="NSE")

    normalized = normalizer.normalize(
        symbol=symbol,
        historical_data=raw_data
    )

    indicators = calculate_indicators(
        normalized["historical"]
    )

    result = analyze_trend(indicators)

    print("\nIndicators:")
    print(indicators)

    print("\nTrend analysis:")
    print(result)

    assert result["trend"] in {
        "UPTREND",
        "DOWNTREND",
        "MIXED",
        "INSUFFICIENT_HISTORY",
        "INSUFFICIENT_DATA",
    }

    assert result["momentum"] in {
        "OVERBOUGHT",
        "OVERSOLD",
        "NEUTRAL",
        "UNKNOWN",
    }

    print("\nPASS: Trend analysis completed successfully.")


if __name__ == "__main__":
    main()
