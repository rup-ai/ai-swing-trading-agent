from datetime import datetime


def format_stock_data(symbol, stock_data):
    """
    Convert raw market API data into a clean stock report.
    """

    if not stock_data:
        return None

    if "error" in stock_data:
        return (
            f"📌 {symbol}\n"
            f"❌ Data error: {stock_data['error']}"
        )

    rows = stock_data.get("data", [])

    if not rows:
        return (
            f"📌 {symbol}\n"
            f"⚠️ No market data available"
        )

    # Use the latest available trading-day record
    latest = rows[-1]

    date = latest.get("date", "N/A")
    open_price = latest.get("open", "N/A")
    high = latest.get("high", "N/A")
    low = latest.get("low", "N/A")
    close = latest.get("close", "N/A")
    prev_close = latest.get("prev_close", "N/A")
    volume = latest.get("volume", "N/A")
    turnover = latest.get("turnover", "N/A")

    # Calculate daily percentage change
    change = "N/A"

    if isinstance(close, (int, float)) and isinstance(
        prev_close, (int, float)
    ):
        if prev_close != 0:
            change_value = ((close - prev_close) / prev_close) * 100
            change = f"{change_value:+.2f}%"

    return (
        f"📊 {symbol}\n\n"
        f"📅 Latest available: {date}\n\n"
        f"💰 Close: ₹{close}\n"
        f"📈 Change: {change}\n\n"
        f"🔺 High: ₹{high}\n"
        f"🔻 Low: ₹{low}\n"
        f"🔹 Open: ₹{open_price}\n\n"
        f"📦 Volume: {volume}\n"
        f"💵 Turnover: ₹{turnover}\n"
        f"\n━━━━━━━━━━━━━━━━"
    )


def format_market_report(market_data, max_stocks=10):
    """
    Create a Telegram-friendly market report.
    """

    message_parts = [
        "📊 RUPAI MARKET DATA REPORT",
        "",
        "Source: TejHQ EOD Data",
        "",
    ]

    count = 0

    for symbol, stock_data in market_data.items():

        if count >= max_stocks:
            break

        formatted = format_stock_data(
            symbol,
            stock_data
        )

        if formatted:
            message_parts.append(formatted)
            message_parts.append("")

        count += 1

    return "\n".join(message_parts)
