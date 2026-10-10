
import csv
import io
import requests


class NSEDataSource:
    """Fetch tradable equity symbols from NSE's official CSV."""

    UNIVERSE_URL = (
        "https://nsearchives.nseindia.com/content/equities/EQUITY_L.csv"
    )

    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
        ),
        "Accept": "text/csv,*/*",
        "Referer": "https://www.nseindia.com/",
    }

    def __init__(self):
        self.name = "NSE"
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)

    def get_market_universe(self):
        """Return symbols listed in NSE's equity-segment CSV."""

        try:
            response = self.session.get(
                self.UNIVERSE_URL,
                timeout=30
            )
            response.raise_for_status()

            reader = csv.DictReader(io.StringIO(response.text))

            if not reader.fieldnames:
                raise ValueError("NSE CSV has no header.")

            headers = {
                name.strip().upper(): name
                for name in reader.fieldnames
                if name
            }

            if "SYMBOL" not in headers:
                raise ValueError(
                    f"SYMBOL column missing. Headers: {reader.fieldnames}"
                )

            symbol_column = headers["SYMBOL"]
            series_column = headers.get("SERIES")
            name_column = headers.get("NAME OF COMPANY")

            stocks = []
            seen = set()

            for row in reader:
                symbol = (row.get(symbol_column) or "").strip().upper()

                if not symbol or symbol in seen:
                    continue

                series = (
                    (row.get(series_column) or "").strip().upper()
                    if series_column else ""
                )

                company_name = (
                    (row.get(name_column) or "").strip()
                    if name_column else ""
                )

                stocks.append({
                    "symbol": symbol,
                    "series": series,
                    "name": company_name,
                    "exchange": "NSE",
                })
                seen.add(symbol)

            if not stocks:
                raise ValueError("NSE CSV returned no symbols.")

            return {
                "source": self.name,
                "status": "success",
                "count": len(stocks),
                "stocks": stocks,
            }

        except (requests.RequestException, ValueError, csv.Error) as error:
            return {
                "source": self.name,
                "status": "error",
                "count": 0,
                "stocks": [],
                "error": str(error),
            }
