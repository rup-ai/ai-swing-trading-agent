import time
import requests


class MarketDataSource:
    """
    Free Indian market-data provider.

    TejHQ keyless API
    Provides NSE/BSE end-of-day OHLCV data.
    """

    BASE_URL = "https://api.tejhq.dev/v1"

    def __init__(self):
        self.name = "TejHQ"

        # Reuse one HTTP connection instead of creating
        # a new connection for every stock.
        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": "RupAI-Market-Intelligence/1.0"
        })

    def get_stock(self, symbol, exchange="NSE"):
        """
        Get historical OHLCV data for one stock.
        """

        url = (
            f"{self.BASE_URL}/ohlcv/"
            f"{exchange.lower()}/{symbol}"
        )

        max_attempts = 3

        for attempt in range(1, max_attempts + 1):

            try:

                response = self.session.get(
                    url,
                    timeout=30
                )

                response.raise_for_status()

                return response.json()

            except requests.RequestException as error:

                if attempt == max_attempts:
                    raise error

                # Wait before retrying
                time.sleep(2)

    def get_multiple_stocks(
        self,
        symbols,
        exchange="NSE",
        delay=0.15
    ):
        """
        Collect market data for multiple stocks.

        Uses controlled requests to reduce the chance
        of hitting provider limits.
        """

        results = {}

        total = len(symbols)

        for index, symbol in enumerate(symbols, start=1):

            try:

                data = self.get_stock(
                    symbol,
                    exchange
                )

                results[symbol] = data

                print(
                    f"✅ [{index}/{total}] {symbol}"
                )

            except Exception as error:

                results[symbol] = {
                    "error": str(error)
                }

                print(
                    f"❌ [{index}/{total}] "
                    f"{symbol}: {error}"
                )

            # Small delay between requests
            if index < total:
                time.sleep(delay)

        return results
