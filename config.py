# RupAI Market Intelligence
# Project configuration

PROJECT_NAME = "RupAI Market Intelligence"

# Trading horizons
SHORT_TERM = "Short Term"
MEDIUM_TERM = "Medium Term"
LONG_TERM = "Long Term"

# Initial stock universe
MARKET = "INDIA"
EXCHANGES = ["NSE", "BSE"]

# Telegram
TELEGRAM_ENABLED = True

# We will add market-data sources here later.
DATA_SOURCES = {
    "nse": True,
    "bse": True,
    "chartink": True,
    "screener": True,
    "moneycontrol": True,
    "nifty_max_pain": True,
    "tickertape": True,
    "tradingview": True,
    "upstox_max_pain": True,
}
