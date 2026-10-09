
# RupAI Market Intelligence
# Moneycontrol stock-page data extraction

import re
from html import unescape

import requests


class MoneycontrolDataSource:
    """Extract labelled market metrics from a public stock page."""

    BASE_URL = "https://www.moneycontrol.com"

    RELIANCE_URL = (
        "https://www.moneycontrol.com/"
        "india/stockpricequote/refineries/relianceindustries/RI"
    )

    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-IN,en;q=0.9",
    }

    METRICS = {
        "open": ["Open"],
        "previous_close": ["Previous Close"],
        "volume": ["Volume"],
        "market_cap_crore": ["Mkt Cap (Rs. Cr.)"],
        "high": ["High"],
        "low": ["Low"],
        "week_52_high": ["52 Week High"],
        "week_52_low": ["52 Week Low"],
        "face_value": ["Face Value"],
        "book_value_per_share": ["Book Value Per Share"],
        "dividend_yield": ["Dividend Yield"],
        "ttm_pe": ["TTM PE"],
        "price_to_book": ["P/B"],
        "sector_pe": ["Sector PE"],
    }

    def __init__(self):
        self.name = "Moneycontrol"
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)

    def get_page(self, url):
        if not url.startswith(self.BASE_URL + "/"):
            raise ValueError("Invalid Moneycontrol URL")

        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        return response.text

    @staticmethod
    def _clean_text(html):
        html = re.sub(
            r"<script\b[^>]*>.*?</script>",
            " ",
            html,
            flags=re.IGNORECASE | re.DOTALL,
        )
        html = re.sub(
            r"<style\b[^>]*>.*?</style>",
            " ",
            html,
            flags=re.IGNORECASE | re.DOTALL,
        )
        html = re.sub(r"<[^>]+>", " ", html)
        html = unescape(html)
        return re.sub(r"\s+", " ", html).strip()

    @staticmethod
    def _extract_metric(text, labels):
        number = r"([-+]?\d[\d,]*(?:\.\d+)?%?)"

        for label in labels:
            pattern = (
                r"(?<![\w])"
                + re.escape(label)
                + r"\s*(?:\|\s*|:\s*)"
                + number
                + r"(?![\w])"
            )

            match = re.search(pattern, text, flags=re.IGNORECASE)

            if match:
                return match.group(1)

        return None

    def get_stock_data(self, url=None):
        url = url or self.RELIANCE_URL
        html = self.get_page(url)
        text = self._clean_text(html)

        title_match = re.search(
            r"<title[^>]*>(.*?)</title>",
            html,
            flags=re.IGNORECASE | re.DOTALL,
        )

        title = (
            unescape(re.sub(r"\s+", " ", title_match.group(1))).strip()
            if title_match
            else None
        )

        fundamentals = {
            key: self._extract_metric(text, labels)
            for key, labels in self.METRICS.items()
        }

        extracted_count = sum(
            value is not None for value in fundamentals.values()
        )

        if extracted_count == 0:
            raise ValueError(
                "Page loaded, but no labelled metrics were extracted. "
                "The page structure may have changed."
            )

        return {
            "source": self.name,
            "status": "success",
            "title": title,
            "fundamentals": fundamentals,
            "metrics_extracted": extracted_count,
            "source_url": url,
            "note": (
                "Extracted displayed page values. Their freshness and "
                "accuracy have not been independently verified."
            ),
        }

    def get_page_data(self, url):
        """Keep the original page-connection test available."""
        html = self.get_page(url)
        text = self._clean_text(html)

        title_match = re.search(
            r"<title[^>]*>(.*?)</title>",
            html,
            flags=re.IGNORECASE | re.DOTALL,
        )

        title = (
            unescape(re.sub(r"\s+", " ", title_match.group(1))).strip()
            if title_match
            else None
        )

        return {
            "source": self.name,
            "status": "connected",
            "title": title,
            "content_length": len(html),
            "page_text_preview": text[:1000],
        }
