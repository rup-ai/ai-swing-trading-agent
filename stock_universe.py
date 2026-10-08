# RupAI Market Intelligence
# Initial Indian stock universe

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


def get_initial_universe():
    """
    Returns the initial list of Indian stocks.
    This list will later be replaced/expanded
    automatically using an official market universe.
    """
    return NSE_SYMBOLS
