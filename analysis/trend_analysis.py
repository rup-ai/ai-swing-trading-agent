
def analyze_trend(indicators):
    """
    Classify trend using moving averages and RSI.
    This is an initial rule-based analysis, not a
    standalone buy/sell recommendation.
    """

    latest_close = indicators.get("latest_close")
    sma_20 = indicators.get("sma_20")
    sma_50 = indicators.get("sma_50")
    rsi = indicators.get("rsi_14")

    if latest_close is None or rsi is None:
        return {
            "trend": "INSUFFICIENT_DATA",
            "momentum": "UNKNOWN",
            "notes": ["Required price indicators are missing."]
        }

    if sma_20 is not None and sma_50 is not None:
        if latest_close > sma_20 > sma_50:
            trend = "UPTREND"
        elif latest_close < sma_20 < sma_50:
            trend = "DOWNTREND"
        else:
            trend = "MIXED"
    else:
        trend = "INSUFFICIENT_HISTORY"

    if rsi >= 70:
        momentum = "OVERBOUGHT"
    elif rsi <= 30:
        momentum = "OVERSOLD"
    else:
        momentum = "NEUTRAL"

    return {
        "trend": trend,
        "momentum": momentum,
        "notes": [
            "Trend and RSI are descriptive indicators, not guaranteed predictions."
        ]
    }
