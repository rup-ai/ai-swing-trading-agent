
# RupAI Market Intelligence
# Screener.in fundamental data extraction

import re
from html.parser import HTMLParser

import requests


class _RatioParser(HTMLParser):
    """Extract ratio names and values from Screener.in HTML."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ratios = {}
        self.current_li = False
        self.current_class = None
        self.current_text = []
        self.current_name = ""
        self.current_value = ""
        self.li_depth = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        if tag == "li" and "data-source" in attrs:
            self.current_li = True
            self.li_depth = 1
            self.current_name = ""
            self.current_value = ""
        elif self.current_li and tag == "li":
            self.li_depth += 1

        if self.current_li and tag == "span":
            classes = attrs.get("class", "").split()
            if "name" in classes:
                self.current_class = "name"
                self.current_text = []
            elif "value" in classes:
                self.current_class = "value"
                self.current_text = []

    def handle_data(self, data):
        if self.current_li and self.current_class:
            self.current_text.append(data)

    def handle_endtag(self, tag):
        if self.current_li and tag == "span" and self.current_class:
            value = " ".join(" ".join(self.current_text).split())

            if self.current_class == "name":
                self.current_name = value
            elif self.current_class == "value":
                self.current_value = value

            self.current_class = None
            self.current_text = []

        if self.current_li and tag == "li":
            self.li_depth -= 1

            if self.li_depth <= 0:
                if self.current_name and self.current_value:
                    self.ratios[self.current_name] = self.current_value
                self.current_li = False
                self.current_class = None


class ScreenerDataSource:
    """
    Retrieve public company fundamentals from Screener.in.

    Values are returned as displayed on the source website.
    Missing values are not replaced with zero.
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
        self.session.headers.update(self.HEADERS)

    def get_company_page(self, symbol):
        symbol = symbol.strip().upper()

        if not re.fullmatch(r"[A-Z0-9&.-]+", symbol):
            raise ValueError("Invalid company symbol")

        urls = [
            f"{self.BASE_URL}/company/{symbol}/consolidated/",
            f"{self.BASE_URL}/company/{symbol}/",
        ]

        last_error = None

        for url in urls:
            try:
                response = self.session.get(url, timeout=30)
                response.raise_for_status()

                if "company-ratios" in response.text or "top-ratios" in response.text:
                    return response.text

                last_error = ValueError(
                    f"Company ratios were not found for {symbol}"
                )

            except requests.RequestException as error:
                last_error = error

        raise RuntimeError(
            f"Could not retrieve company page for {symbol}: {last_error}"
        )

    def get_company_data(self, symbol):
        page = self.get_company_page(symbol)

        parser = _RatioParser()
        parser.feed(page)

        ratios = parser.ratios

        if not ratios:
            raise ValueError(
                "The page loaded, but no fundamental ratios were extracted. "
                "The website HTML may have changed or access may be restricted."
            )

        def find_ratio(*possible_names):
            for name, value in ratios.items():
                if name.strip().lower() in {
                    candidate.lower() for candidate in possible_names
                }:
                    return value
            return None

        fundamentals = {
            "market_cap": find_ratio("Market Cap"),
            "current_price": find_ratio("Current Price"),
            "stock_pe": find_ratio("Stock P/E", "P/E"),
            "book_value": find_ratio("Book Value"),
            "dividend_yield": find_ratio("Dividend Yield"),
            "roe": find_ratio("ROE"),
            "roce": find_ratio("ROCE"),
            "face_value": find_ratio("Face Value"),
            "high_low": find_ratio("High / Low"),
        }

        return {
            "source": self.name,
            "symbol": symbol.strip().upper(),
            "status": "success",
            "fundamentals": fundamentals,
            "all_top_ratios": ratios,
            "ratios_extracted": len(ratios),
            "source_url": (
                f"{self.BASE_URL}/company/{symbol.strip().upper()}/"
            ),
        }
