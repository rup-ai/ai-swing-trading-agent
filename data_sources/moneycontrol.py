
# RupAI Market Intelligence
# Moneycontrol public-page data connector

import re
from html import unescape

import requests


class MoneycontrolDataSource:
    """Fetch and inspect publicly accessible Moneycontrol pages."""

    BASE_URL = "https://www.moneycontrol.com"

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
            raise ValueError("Please provide a valid Moneycontrol page URL.")

        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        return response.text

    def get_page_data(self, url):
        """Return basic page metadata, not verified live stock prices."""

        html = self.get_page(url)

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

        text = re.sub(r"<script\b[^>]*>.*?</script>", " ", html,
                      flags=re.IGNORECASE | re.DOTALL)
        text = re.sub(r"<style\b[^>]*>.*?</style>", " ", text,
                      flags=re.IGNORECASE | re.DOTALL)
        text = re.sub(r"<[^>]+>", " ", text)
        text = unescape(re.sub(r"\s+", " ", text)).strip()

        if not title and not text:
            raise ValueError(
                "The page loaded, but no readable content was found."
            )

        return {
            "source": self.name,
            "status": "connected",
            "title": title,
            "content_length": len(html),
            "page_text_preview": text[:1000],
            "note": (
                "Page connection test only. "
                "Live price and fundamental fields are not yet verified."
            ),
        }
