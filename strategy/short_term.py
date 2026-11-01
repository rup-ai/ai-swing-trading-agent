
from math import isfinite


def calculate_atr(historical_data, period=14):
    """
    Calculate Average True Range (ATR).
    historical_data must contain daily OHLC data.
    """
    if not isinstance(historical_data, list) or len(historical_data) < period + 1:
        return None

    true_ranges = []
    previous_close = None

    for row in historical_data:
        try:
            high = float(row["high"])
            low = float(row["low"])
            close = float(row["close"])

            if not all(isfinite(value) for value in (high, low, close)):
                return None

            if high < low:
                return None

            if previous_close is None:
                true_range = high - low
            else:
                true_range = max(
                    high - low,
                    abs(high - previous_close),
                    abs(low - previous_close)
                )

            true_ranges.append(true_range)
            previous_close = close

        except (KeyError, TypeError, ValueError):
            return None

    if len(true_ranges) < period:
        return None

    return sum(true_ranges[-period:]) / period


def generate_trade_setup(analysis_result, historical_data):
    """
    Generate an experimental 4-7 trading day swing-trade setup.
    This is a screening rule, not a guaranteed trading signal.
    """
    if analysis_result.get("status") != "SUCCESS":
        return {
            "symbol": analysis_result.get("symbol", "UNKNOWN"),
            "signal": "NO_TRADE",
            "reason": "Stock analysis was unsuccessful."
        }

    indicators = analysis_result.get("indicators", {})

    try:
        entry = float(indicators["close"])
        sma20 = float(indicators["sma_20"])
        sma50 = float(indicators["sma_50"])
        rsi = float(indicators["rsi_14"])
    except (KeyError, TypeError, ValueError):
        return {
            "symbol": analysis_result.get("symbol", "UNKNOWN"),
            "signal": "NO_TRADE",
            "reason": "Required technical indicators are unavailable."
        }

    if not all(isfinite(value) for value in (entry, sma20, sma50, rsi)):
        return {
            "symbol": analysis_result.get("symbol", "UNKNOWN"),
            "signal": "NO_TRADE",
            "reason": "Invalid technical indicator values."
        }

    atr = calculate_atr(historical_data, period=14)

    if atr is None or atr <= 0:
        return {
            "symbol": analysis_result.get("symbol", "UNKNOWN"),
            "signal": "NO_TRADE",
            "reason": "Insufficient or invalid ATR data."
        }

    if not (entry > sma20 > sma50):
        return {
            "symbol": analysis_result.get("symbol", "UNKNOWN"),
            "signal": "NO_TRADE",
            "reason": "Trend filter not satisfied: close must be above SMA20 and SMA50."
        }

    if not (50 <= rsi <= 68):
        return {
            "symbol": analysis_result.get("symbol", "UNKNOWN"),
            "signal": "NO_TRADE",
            "reason": "RSI is outside the experimental 50-68 range."
        }

    stop_loss = entry - (1.5 * atr)
    risk = entry - stop_loss
    target = entry + (2 * risk)

    if stop_loss <= 0 or risk <= 0:
        return {
            "symbol": analysis_result.get("symbol", "UNKNOWN"),
            "signal": "NO_TRADE",
            "reason": "Calculated risk levels are invalid."
        }

    return {
        "symbol": analysis_result.get("symbol", "UNKNOWN"),
        "signal": "BUY_CANDIDATE",
        "entry": round(entry, 2),
        "stop_loss": round(stop_loss, 2),
        "target": round(target, 2),
        "risk_per_share": round(risk, 2),
        "reward_risk_ratio": 2.0,
        "atr_14": round(atr, 2),
        "rsi_14": round(rsi, 2),
        "holding_period": "4-7 trading days",
        "reason": "Uptrend, RSI filter and ATR-based risk filters passed."
    }
