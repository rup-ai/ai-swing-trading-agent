
from analysis.technical_indicators import calculate_indicators
from analysis.trend_analysis import analyze_trend


def analyze_stock(normalized_data):
    """
    Analyze one stock using normalized historical data.
    Returns indicators and descriptive trend analysis.
    """

    symbol = normalized_data.get("symbol", "UNKNOWN")
    historical = normalized_data.get("historical", [])

    if not historical:
        return {
            "symbol": symbol,
            "status": "INSUFFICIENT_DATA",
            "message": "No historical data available."
        }

    try:
        indicators = calculate_indicators(historical)
        trend = analyze_trend(indicators)

        return {
            "symbol": symbol,
            "status": "SUCCESS",
            "indicators": indicators,
            "analysis": trend
        }

    except (ValueError, KeyError, TypeError) as error:
        return {
            "symbol": symbol,
            "status": "ANALYSIS_FAILED",
            "message": str(error)
        }
