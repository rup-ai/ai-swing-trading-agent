
from providers.market_api import MarketDataSource
from providers.data_normalizer import MarketDataNormalizer


def main():
    symbol = "RELIANCE"

    print("Testing real API data for", symbol)

    api = MarketDataSource()
    normalizer = MarketDataNormalizer()

    raw_data = api.get_stock(symbol, exchange="NSE")

    result = normalizer.normalize(
        symbol=symbol,
        historical_data=raw_data
    )

    rows = result["historical"]

    if not rows:
        raise AssertionError("No historical records returned")

    required_fields = [
        "date", "open", "high", "low", "close", "volume"
    ]

    for row in rows:
        missing = [
            field for field in required_fields
            if row.get(field) is None
        ]
        if missing:
            raise AssertionError(
                f"Missing fields in {row.get('date')}: {missing}"
            )

    dates = [row["date"] for row in rows]

    if dates != sorted(dates):
        raise AssertionError(
            "Historical records are not oldest-to-newest"
        )

    print("PASS: Normalizer accepted real API data")
    print("Symbol:", result["symbol"])
    print("Records:", len(rows))
    print("First date:", dates[0])
    print("Latest date:", dates[-1])
    print("Required OHLCV fields: present")


if __name__ == "__main__":
    main()
