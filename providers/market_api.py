import requests


API_URL = "https://indian-stock-market-api.onrender.com"


class MarketDataSource:
    """
    Free market-data connector for NSE/BSE stocks.

    This is currently used for the first market-data pipeline test.
    Later, additional validated sources will be added.
    """

    def __init__(self):
        self.base_url = API_URL

    def get_stock(self, symbol):
        """
        Get data for one stock.
        """
        url = f"{self.base_url}/stock"

        response = requests.get(
            url,
            params={
                "symbol": symbol,
                "res": "num"
            },
            timeout=20
        )

        response.raise_for_status()
        return response.json()

    def get_multiple_stocks(self, symbols):
        """
        Get data for multiple stocks in one request.
        """

        url = f"{self.base_url}/stock/list"

        response = requests.get(
            url,
            params={
                "symbols": ",".join(symbols),
                "res": "num"
            },
            timeout=30
        )

        response.raise_for_status()
        return response.json()
