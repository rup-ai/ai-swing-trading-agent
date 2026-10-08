# RupAI Market Intelligence
# Screener.in fundamental data source

import requests


class ScreenerDataSource:
    """
    Screener.in connector.

    Used for fundamental stock-screening data
    and public company information.
    """

    BASE_URL = "https://www.screener.in"

    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "Chrome/120.0 Safari/537.36"
        ),
        "Accept": (
            "text/html,application/xhtml+xml,"
            "application/xml;q=0.9,*/*;q=0.8"
        ),
    }

    def __init__(self):
        self.name = "Screener.in"

        self.session = requests.Session()

        self.session.headers.update(
            self.HEADERS
        )

    def get_company_page(self, symbol):
        """
        Get the public company page from Screener.in.

        Example:
            RELIANCE
            TCS
            INFY
        """

        url = f"{self.BASE_URL}/company/{symbol}/"

        response = self.session.get(
            url,
            timeout=30
        )

        response.raise_for_status()

        return response.text

    def get_company_data(self, symbol):
        """
        Retrieve basic public company-page information.

        Detailed fundamental parsing will be added
        after the connector test succeeds.
        """

        page = self.get_company_page(
            symbol
        )

        return {
            "source": self.name,
            "symbol": symbol,
            "status": "connected",
            "content_length": len(page),
        }
