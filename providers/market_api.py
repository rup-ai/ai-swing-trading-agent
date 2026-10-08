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

    def get_stock(self, symbol, exchange="NSE"):
        """
        Get historical OHLCV data for one stock.
        """

        url = f"{self.BASE_URL}/ohlcv/{exchange.lower()}/{symbol}"

        response = requests.get(
            url,
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    def get_multiple_stocks(self, symbols, exchange="NSE"):
        """
        Get market data for multiple stocks.
        """

        results = {}

        for symbol in symbols:
            try:
                data = self.get_stock(symbol, exchange)
                results[symbol] = data

            except Exception as error:
                results[symbol] = {
                    "error": str(error)
                }

        return results
