
def score_stock(analysis_result):
    """
    Initial rule-based stock score from 0 to 100.
    This is a research ranking, not a buy/sell signal.
    """

    if analysis_result.get("status") != "SUCCESS":
        return {
            "symbol": analysis_result.get("symbol", "UNKNOWN"),
            "score": None,
            "rating": "NOT_RANKED",
            "reasons": ["Analysis data unavailable."]
        }

    indicators = analysis_result.get("indicators", {})
    analysis = analysis_result.get("analysis", {})

    score = 50
    reasons = []

    latest_close = indicators.get("latest_close")
    sma_20 = indicators.get("sma_20")
    sma_50 = indicators.get("sma_50")
    rsi = indicators.get("rsi_14")
    trend = analysis.get("trend")
    momentum = analysis.get("momentum")

    if latest_close is None or rsi is None:
        return {
            "symbol": analysis_result.get("symbol", "UNKNOWN"),
            "score": None,
            "rating": "NOT_RANKED",
            "reasons": ["Required indicators are missing."]
        }

    if sma_20 is not None and latest_close > sma_20:
        score += 10
        reasons.append("Price above 20-day SMA.")
    elif sma_20 is not None:
        score -= 10
        reasons.append("Price below 20-day SMA.")

    if sma_50 is not None and latest_close > sma_50:
        score += 10
        reasons.append("Price above 50-day SMA.")
    elif sma_50 is not None:
        score -= 10
        reasons.append("Price below 50-day SMA.")

    if trend == "UPTREND":
        score += 15
        reasons.append("Moving-average trend is positive.")
    elif trend == "DOWNTREND":
        score -= 15
        reasons.append("Moving-average trend is negative.")

    if 50 <= rsi < 70:
        score += 10
        reasons.append("RSI indicates positive momentum.")
    elif rsi >= 70:
        score -= 5
        reasons.append("RSI is elevated; pullback risk may be higher.")
    elif rsi < 30:
        reasons.append("RSI is low; weakness or a reversal is possible.")
    else:
        score -= 5
        reasons.append("RSI momentum is below the neutral threshold.")

    score = max(0, min(100, score))

    if score >= 75:
        rating = "HIGHER_RANKED"
    elif score >= 60:
        rating = "MODERATE"
    else:
        rating = "LOWER_RANKED"

    return {
        "symbol": analysis_result.get("symbol", "UNKNOWN"),
        "score": score,
        "rating": rating,
        "reasons": reasons
    }
