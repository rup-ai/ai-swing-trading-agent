
from math import isfinite


def calculate_sma(values, period):
    """Calculate a simple moving average."""
    if len(values) < period:
        return None

    recent = values[-period:]

    if not all(isfinite(v) for v in recent):
        return None

    return round(sum(recent) / period, 2)


def calculate_rsi(closes, period=14):
    """Calculate RSI using average gains and losses."""
    if len(closes) < period + 1:
        return None

    changes = [
        closes[i] - closes[i - 1]
        for i in range(len(closes) - period, len(closes))
    ]

    gains = [max(change, 0) for change in changes]
    losses = [max(-change, 0) for change in changes]

    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period

    if avg_loss == 0:
        return 100.0 if avg_gain > 0 else 50.0

    rs = avg_gain / avg_loss
    return round(100 - (100 / (1 + rs)), 2)


def calculate_indicators(historical_data):
    """
    Calculate initial technical indicators from normalized
    historical OHLCV records.
    """

    rows = sorted(
        historical_data,
        key=lambda row: row["date"]
    )

    closes = [
        float(row["close"])
        for row in rows
        if row.get("close") is not None
    ]

    if len(closes) < 15:
        raise ValueError(
            "At least 15 valid closing prices are required."
        )

    latest_close = closes[-1]

    return {
        "latest_close": round(latest_close, 2),
        "sma_20": calculate_sma(closes, 20),
        "sma_50": calculate_sma(closes, 50),
        "rsi_14": calculate_rsi(closes, 14),
        "records_used": len(closes),
    }
