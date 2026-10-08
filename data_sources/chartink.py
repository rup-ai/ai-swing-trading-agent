# RupAI Market Intelligence
# Chartink technical screening layer

import requests


class ChartinkDataSource:
    """
    Chartink technical screening connector.

    Used to retrieve technical scanner results.
    """

    BASE_URL = "https://chartink.com"

    def __init__(self):
        self.name = "Chartink"

        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "Chrome/120.0 Safari/537.36"
            ),
            "Referer": "https://chartink.com/",
        })

    def get_scan_page(self, scan_url):
        """
        Fetch a Chartink scanner page.

        scan_url should be a public Chartink scanner URL.
        """

        response = self.session.get(
            scan_url,
            timeout=30
        )

        response.raise_for_status()

        return response.text

    def get_scan_results(self, scan_url):
        """
        Retrieve the scanner page content.

        Scanner parsing will be added after
        the connection test succeeds.
        """

        page = self.get_scan_page(
            scan_url
        )

        return {
            "source": self.name,
            "status": "connected",
            "url": scan_url,
            "content_length": len(page),
        }
