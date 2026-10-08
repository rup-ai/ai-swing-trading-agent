# RupAI Market Intelligence
# BSE data source layer

import requests


class BSEDataSource:
    """
    BSE market-data connector.

    Used to retrieve recent market information
    from BSE's public endpoints.
    """

    BASE_URL = "https://api.bseindia.com"

    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "Chrome/120.0 Safari/537.36"
        ),
        "Accept": "application/json",
        "Referer": "https://www.bseindia.com/",
    }

    def __init__(self):
        self.name = "BSE"

        self.session = requests.Session()

        self.session.headers.update(
            self.HEADERS
        )

    def get_stock_data(self, scrip_code):
        """
        Get recent market data for one BSE stock.

        scrip_code should be the BSE numeric
        security code, for example 500325.
        """

        url = (
            f"{self.BASE_URL}/BseIndiaAPI/api/"
            f"StockReachGraph/w?scripcode="
            f"{scrip_code}&flag=0&fromdate=&todate="
        )

        response = self.session.get(
            url,
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    def get_stock_quote(self, scrip_code):
        """
        Get quote information for a BSE security.
        """

        url = (
            f"{self.BASE_URL}/BseIndiaAPI/api/"
            f"getScripHeaderData/w"
            f"?scripcode={scrip_code}"
        )

        response = self.session.get(
            url,
            timeout=30
        )

        response.raise_for_status()

        return response.json()
