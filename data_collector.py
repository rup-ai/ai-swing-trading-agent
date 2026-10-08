from stock_universe import get_initial_universe
from providers.market_api import MarketDataSource


def collect_market_data():
    """
    Collect current market data for all stocks
    in our current stock universe.
    """

    symbols = get_initial_universe()

    market_api = MarketDataSource()

    print(f"Scanning {len(symbols)} stocks...")

    try:
        data = market_api.get_multiple_stocks(symbols)

        print("Market data received successfully.")

        return data

    except Exception as error:
        print(f"Market data collection failed: {error}")
        return None


if __name__ == "__main__":
    market_data = collect_market_data()

    if market_data:
        print("\n===== MARKET DATA =====")
        print(market_data)
