
# RupAI Market Intelligence
# Moneycontrol public stock-page extraction

import re
from html import unescape

import requests


class MoneycontrolDataSource:
    """Fetch public stock pages and extract displayed market values."""

    BASE_URL = "https://www.moneycontrol.com"

    RELIANCE_URL = (
        "https://www.moneycontrol.com/"
        "india/stockpricequote/refineries/"
        "relianceindustries/RI"
    )

    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-IN,en;q=0.9",
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
        html = re.sub(r"<!--.*?-->", " ", html, flags=re.DOTALL)
        html = re.sub(r"<[^>]+>", " ", html)
        html = unescape(html)
        return re.sub(r"\s+", " ", html).strip()

    @staticmethod
    def _search(pattern, text, group=1):
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return match.group(group).strip()
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

        number = r"([\d,]+(?:\.\d+)?)"
        percent = r"([-+]?\d+(?:\.\d+)?%)"

        # Quote pattern seen on the stock page:
        # price, absolute change, percentage change, "As on" timestamp.
        quote_pattern = (
            number
            + r"\s+([-+]?[\d,]+(?:\.\d+)?)\s*"
            + r"\((" + r"[-+]?\d+(?:\.\d+)?%" + r")\)\s+"
            + r"As on\s+(.{1,50}?)(?=\s+(?:Open Trading|Day Range|52 Week Range))"
        )

        quote = re.search(
            quote_pattern,
            text,
            flags=re.IGNORECASE,
        )

        displayed_price = quote.group(1) if quote else None
        price_change = quote.group(2) if quote else None
        change_percent = quote.group(3) if quote else None
        as_of = (
            re.sub(r"\s+", " ", quote.group(4)).strip()
            if quote
            else None
        )

        day_range = re.search(
            r"Day Range\s+" + number + r"\s+" + number,
            text,
            flags=re.IGNORECASE,
        )

        week_range = re.search(
            r"52 Week Range\s+" + number + r"\s+" + number,
            text,
            flags=re.IGNORECASE,
        )

        volume = self._search(
            r"Volume\s+" + number,
            text,
        )

        fundamentals = {
            "displayed_price": displayed_price,
            "price_change": price_change,
            "change_percent": change_percent,
            "as_of": as_of,
            "day_range_low": day_range.group(1) if day_range else None,
            "day_range_high": day_range.group(2) if day_range else None,
            "week_52_low": week_range.group(1) if week_range else None,
            "week_52_high": week_range.group(2) if week_range else None,
            "volume": volume,
        }

        extracted_count = sum(
            value is not None for value in fundamentals.values()
        )

        return {
            "source": self.name,
            "status": "success" if extracted_count else "no_metrics_found",
            "title": title,
            "fundamentals": fundamentals,
            "metrics_extracted": extracted_count,
            "source_url": url,
            "page_length": len(html),
            "page_text_preview": text[:1200] if not extracted_count else None,
            "note": (
                "Displayed values extracted; freshness and accuracy "
                "have not been independently verified."
            ),
        }

    def get_page_data(self, url):
        """Keep the original page connection test available."""
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
