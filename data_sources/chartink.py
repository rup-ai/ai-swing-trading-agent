# RupAI Market Intelligence
# Chartink technical screening layer

import re
import requests


class ChartinkDataSource:
    """
    Chartink technical screening connector.

    Used to retrieve public Chartink scanner results.
    """

    BASE_URL = "https://chartink.com"

    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "Chrome/120.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,"
                  "application/xml;q=0.9,*/*;q=0.8",
        "Referer": "https://chartink.com/",
    }

    def __init__(self):
        self.name = "Chartink"

        self.session = requests.Session()

        self.session.headers.update(
            self.HEADERS
        )

    def get_scan_page(self, scan_url):
        """
        Fetch a public Chartink scanner page.
        """

        response = self.session.get(
            scan_url,
            timeout=30
        )

        response.raise_for_status()

        return response.text

    def get_scan_results(self, scan_url):
        """
        Fetch a Chartink scanner page and extract
        stock symbols that are visible in the page.
        """

        page = self.get_scan_page(
            scan_url
        )

        symbols = self._extract_symbols(page)

        return {
            "source": self.name,
            "status": "connected",
            "url": scan_url,
            "stocks": symbols,
            "count": len(symbols),
        }

    def _extract_symbols(self, html):
        """
        Basic symbol extraction from the returned
        Chartink HTML.

        This is intentionally conservative.
        """

        symbols = set()

        # Look for common NSE symbol attributes
        patterns = [
            r'data-symbol=["\']([A-Z0-9&-]+)["\']',
            r'"symbol"\s*:\s*"([A-Z0-9&-]+)"',
            r"'symbol'\s*:\s*'([A-Z0-9&-]+)'",
        ]

        for pattern in patterns:

            matches = re.findall(
                pattern,
                html,
                flags=re.IGNORECASE
            )

            for symbol in matches:

                symbol = symbol.upper().strip()

                if (
                    1 <= len(symbol) <= 30
                    and symbol not in {
                        "NSE",
                        "BSE",
                        "NULL",
                        "UNDEFINED"
                    }
                ):
                    symbols.add(symbol)

        return sorted(symbols)
