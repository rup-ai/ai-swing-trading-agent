
# RupAI Market Intelligence
# Dynamic Indian stock universe

import csv
import io
import requests

from data_sources.nse import NSEDataSource


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


# Existing backup list — preserved.
NSE_SYMBOLS = [
    "RELIANCE", "TCS", "HDFCBANK", "ICICIBANK", "INFY",
    "ITC", "SBIN", "BHARTIARTL", "LT", "AXISBANK",
    "KOTAKBANK", "HINDUNILVR", "MARUTI", "M&M",
    "SUNPHARMA", "TATAMOTORS", "TATASTEEL", "ADANIENT",
    "ADANIPORTS", "NTPC", "POWERGRID", "ONGC", "COALINDIA",
    "WIPRO", "HCLTECH", "TECHM", "BAJFINANCE",
    "BAJAJFINSV", "ASIANPAINT", "ULTRACEMCO", "TITAN",
    "NESTLEIND", "JSWSTEEL", "GRASIM", "CIPLA", "DRREDDY",
    "EICHERMOT", "HEROMOTOCO", "BAJAJ-AUTO",
]


def get_nifty500_universe():
    """Fetch current NIFTY 500 constituents from NSE."""

    session = requests.Session()

    try:
        session.get(
            "https://www.nseindia.com/",
            headers=HEADERS,
            timeout=20,
        )

        response = session.get(
            NSE_EQUITY_URL,
            headers=HEADERS,
            timeout=30,
        )
        response.raise_for_status()

        payload = response.json()
        stocks = [
            item["symbol"].strip().upper()
            for item in payload.get("data", [])
            if item.get("symbol")
        ]
        stocks = list(dict.fromkeys(stocks))

        if stocks:
            print(f"NSE NIFTY 500 loaded: {len(stocks)} stocks")
            return stocks

    except (requests.RequestException, ValueError, TypeError, KeyError) as error:
        print(f"NSE NIFTY 500 fetch failed: {error}")

    return []


def get_broad_nse_universe():
    """Fetch equity symbols from the official NSE equity CSV."""

    result = NSEDataSource().get_market_universe()

    if result.get("status") != "success":
        print(
            "Broad NSE CSV unavailable:",
            result.get("error", "unknown error"),
        )
        return []

    stocks = result.get("stocks", [])

    # Restrict to ordinary equity series supported by the CSV.
    symbols = [
        item["symbol"].strip().upper()
        for item in stocks
        if item.get("symbol")
        and item.get("series", "").strip().upper() in {"EQ", "BE"}
    ]

    symbols = list(dict.fromkeys(symbols))

    if symbols:
        print(f"Broad NSE equity universe loaded: {len(symbols)} symbols")

    return symbols


def get_initial_universe():
    """Prefer broad NSE equity coverage, then NIFTY 500, then backup."""

    symbols = get_broad_nse_universe()

    if symbols:
        return symbols

    symbols = get_nifty500_universe()

    if symbols:
        print("Using NIFTY 500 as the fallback universe.")
        return symbols

    print(f"Using backup universe: {len(NSE_SYMBOLS)} stocks")
    return NSE_SYMBOLS.copy()
