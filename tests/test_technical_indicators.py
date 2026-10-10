
from providers.market_api import MarketDataSource
from providers.data_normalizer import MarketDataNormalizer
from analysis.technical_indicators import calculate_indicators


def main():
    symbol = "RELIANCE"

    print("Testing technical indicators with real data:", symbol)

    api = MarketDataSource()
    normalizer = MarketDataNormalizer()

    raw_data = api.get_stock(symbol, exchange="NSE")

    normalized = normalizer.normalize(
        symbol=symbol,
        historical_data=raw_data
    )

    result = calculate_indicators(
        normalized["historical"]
    )

    print("\nTechnical indicators:")
    for name, value in result.items():
        print(f"{name}: {value}")

    assert result["latest_close"] > 0
    assert result["records_used"] >= 15
    assert result["rsi_14"] is not None
    assert 0 <= result["rsi_14"] <= 100

    print("\nPASS: Technical indicators calculated successfully.")


if __name__ == "__main__":
    main()
