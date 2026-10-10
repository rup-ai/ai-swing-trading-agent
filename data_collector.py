
from stock_universe import get_initial_universe
from providers.market_api import MarketDataSource


def _classify_result(result):
    """Classify a provider response without changing its raw data."""

    if not result or not isinstance(result, (dict, list)):
        return "empty"

    if isinstance(result, dict):
        if "error" in result:
            return "failed"

        # Common empty-data response format.
        if "data" in result and not result["data"]:
            return "empty"

    if isinstance(result, list) and not result:
        return "empty"

    return "success"


def collect_market_data(symbols=None):
    """
    Collect market data for supplied symbols or the current
    NSE universe. Return the raw provider results.
    """

    if symbols is None:
        symbols = get_initial_universe()

    # Remove duplicates while preserving the original order.
    symbols = list(dict.fromkeys(symbols))

    if not symbols:
        print("No stock symbols available to scan.")
        return {}

    market_api = MarketDataSource()

    print(f"Scanning {len(symbols)} stocks...")

    try:
        data = market_api.get_multiple_stocks(symbols)

        if not isinstance(data, dict):
            print("Market data collection failed: invalid response.")
            return None

        success = 0
        failed = 0
        empty = 0

        for result in data.values():
            status = _classify_result(result)

            if status == "success":
                success += 1
            elif status == "failed":
                failed += 1
            else:
                empty += 1

        print(
            "Market data collection completed. "
            f"Success: {success}, Failed: {failed}, "
            f"Empty: {empty}, "
            f"Returned: {len(data)}, Requested: {len(symbols)}"
        )

        return data

    except Exception as error:
        print(f"Market data collection failed: {error}")
        return None


if __name__ == "__main__":
    market_data = collect_market_data()

    if market_data:
        print("\n===== MARKET DATA SUMMARY =====")
        print(f"Stocks returned: {len(market_data)}")
