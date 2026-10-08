# RupAI Market Intelligence
# Dynamic Indian stock universe

import requests


NSE_EQUITY_URL = (
    "https://www.nseindia.com/api/equity-stockIndices"
    "?index=NIFTY%20500"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "Chrome/120.0 Safari/537.36"
    ),
    "Accept": "application/json",
    "Referer": "https://www.nseindia.com/",
}


# Backup list
# Used only if NSE cannot be accessed.
NSE_SYMBOLS = [
    "RELIANCE",
    "TCS",
    "HDFCBANK",
    "ICICIBANK",
    "INFY",
    "ITC",
    "SBIN",
    "BHARTIARTL",
    "LT",
    "AXISBANK",
    "KOTAKBANK",
    "HINDUNILVR",
    "MARUTI",
    "M&M",
    "SUNPHARMA",
    "TATAMOTORS",
    "TATASTEEL",
    "ADANIENT",
    "ADANIPORTS",
    "NTPC",
    "POWERGRID",
    "ONGC",
    "COALINDIA",
    "WIPRO",
    "HCLTECH",
    "TECHM",
    "BAJFINANCE",
    "BAJAJFINSV",
    "ASIANPAINT",
    "ULTRACEMCO",
    "TITAN",
    "NESTLEIND",
    "JSWSTEEL",
    "GRASIM",
    "CIPLA",
    "DRREDDY",
    "EICHERMOT",
    "HEROMOTOCO",
    "BAJAJ-AUTO",
]


def get_nifty500_universe():
    """
    Fetch the current NIFTY 500 constituents from NSE.
    """

    session = requests.Session()

    try:
        # First visit NSE to establish cookies.
        session.get(
            "https://www.nseindia.com/",
            headers=HEADERS,
            timeout=20
        )

        response = session.get(
            NSE_EQUITY_URL,
            headers=HEADERS,
            timeout=30
        )

        response.raise_for_status()

        payload = response.json()

        stocks = []

        for item in payload.get("data", []):
            symbol = item.get("symbol")

            if symbol:
                stocks.append(symbol)

        # Remove duplicates
        stocks = list(dict.fromkeys(stocks))

        if stocks:
            print(
                f"✅ NSE NIFTY 500 universe loaded: "
                f"{len(stocks)} stocks"
            )

            return stocks

    except Exception as error:
        print(
            "⚠️ NSE universe fetch failed:"
        )
        print(error)

    print(
        f"⚠️ Using backup universe: "
        f"{len(NSE_SYMBOLS)} stocks"
    )

    return NSE_SYMBOLS


def get_initial_universe():
    """
    Returns the current NSE NIFTY 500 universe.
    """

    return get_nifty500_universe()
