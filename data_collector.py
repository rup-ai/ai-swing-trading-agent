from stock_universe import get_initial_universe
from providers.market_api import MarketDataSource


def collect_market_data(symbols=None):
    """
    Collect market data for the provided symbols.

    If no symbols are provided, the complete
    current stock universe is used.
    """

    if symbols is None:
        symbols = get_initial_universe()

    market_api = MarketDataSource()

    print(f"Scanning {len(symbols)} stocks...")

    try:
        data = market_api.get_multiple_stocks(symbols)

        successful = 0
        failed = 0

        for symbol, result in data.items():

            if isinstance(result, dict) and "error" in result:
                failed += 1
            else:
                successful += 1

        print(
            f"Market data collection completed. "
            f"Success: {successful}, Failed: {failed}"
        )

        return data

    except Exception as error:

        print(
            f"Market data collection failed: {error}"
        )

        return None


if __name__ == "__main__":

    market_data = collect_market_data()

    if market_data:

        print("\n===== MARKET DATA =====")

        print(market_data)
