
from providers.data_normalizer import MarketDataNormalizer
from analysis.stock_analyzer import analyze_stock
from analysis.stock_ranker import rank_stocks


def scan_market(market_data):
    """
    Normalize and analyze collected market data,
    then rank stocks with valid analysis results.
    """

    normalizer = MarketDataNormalizer()

    analysis_results = []
    failures = []

    for symbol, raw_data in market_data.items():

        if not isinstance(raw_data, dict) or raw_data.get("error"):
            failures.append({
                "symbol": symbol,
                "reason": (
                    raw_data.get("error", "Invalid market data")
                    if isinstance(raw_data, dict)
                    else "Invalid market data"
                )
            })
            continue

        try:
            normalized = normalizer.normalize(
                symbol=symbol,
                historical_data=raw_data
            )

            result = analyze_stock(normalized)

            if result.get("status") == "SUCCESS":
                analysis_results.append(result)
            else:
                failures.append({
                    "symbol": symbol,
                    "reason": result.get(
                        "message", "Analysis failed"
                    )
                })

        except Exception as error:
            failures.append({
                "symbol": symbol,
                "reason": str(error)
            })

    ranked = rank_stocks(analysis_results)

    return {
        "scanned": len(market_data),
        "analyzed": len(analysis_results),
        "failed": len(failures),
        "ranked_stocks": ranked,
        "failures": failures
    }
