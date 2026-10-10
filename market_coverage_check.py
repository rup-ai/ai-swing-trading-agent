
from providers.market_api import MarketDataSource


SAMPLE_STOCKS = [
    "RELIANCE",
    "TCS",
    "HDFCBANK",
    "ICICIBANK",
    "INFY",
    "SBIN",
    "ITC",
    "LT",
    "BHARTIARTL",
    "WIPRO",
]


def check_stock(symbol, result):
    if not isinstance(result, dict):
        return "INVALID", 0, "Unexpected response format"

    if result.get("error"):
        return "FAILED", 0, str(result["error"])[:120]

    rows = result.get("data", [])

    if not isinstance(rows, list) or not rows:
        return "EMPTY", 0, "No historical candles returned"

    valid_rows = [
        row for row in rows
        if isinstance(row, dict) and row.get("close") is not None
    ]

    if not valid_rows:
        return "EMPTY", len(rows), "No usable closing prices"

    latest_date = max(
        (str(row.get("date", "")) for row in valid_rows),
        default="Unknown",
    )

    return "SUCCESS", len(valid_rows), f"Latest date: {latest_date}"


def main():
    api = MarketDataSource()

    print(f"Testing {len(SAMPLE_STOCKS)} NSE stocks")
    print("-" * 65)

    results = api.get_multiple_stocks(SAMPLE_STOCKS, delay=0.5)

    success = failed = empty = invalid = 0

    for symbol in SAMPLE_STOCKS:
        result = results.get(symbol)

        status, candles, detail = check_stock(symbol, result)

        if status == "SUCCESS":
            success += 1
        elif status == "FAILED":
            failed += 1
        elif status == "EMPTY":
            empty += 1
        else:
            invalid += 1

        print(
            f"{symbol:12} | {status:7} | "
            f"Candles: {candles:3} | {detail}"
        )

    print("-" * 65)
    print(f"Requested: {len(SAMPLE_STOCKS)}")
    print(f"Success:   {success}")
    print(f"Failed:    {failed}")
    print(f"Empty:     {empty}")
    print(f"Invalid:   {invalid}")

    coverage = success / len(SAMPLE_STOCKS) * 100
    print(f"Usable-data coverage: {coverage:.1f}%")

    print(
        "\nNote: This checks data availability, "
        "not trading-signal accuracy."
    )


if __name__ == "__main__":
    main()
