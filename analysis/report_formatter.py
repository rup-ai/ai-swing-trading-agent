
from datetime import datetime, timezone


def format_ranked_report(scan_result, max_stocks=10):
    """Format ranked stocks into a readable market report."""

    ranked = scan_result.get("ranked_stocks", [])

    lines = [
        "📊 RUPAI MARKET INTELLIGENCE",
        "Report: Technical Stock Ranking",
        f"Generated (UTC): {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')}",
        "",
        f"Stocks scanned: {scan_result.get('scanned', 0)}",
        f"Successfully analyzed: {scan_result.get('analyzed', 0)}",
        f"Failed / skipped: {scan_result.get('failed', 0)}",
        "",
        "Note: Ranking is experimental, not a buy/sell recommendation.",
        "",
        "🏆 RANKED STOCKS",
        ""
    ]

    valid_stocks = [
        stock for stock in ranked
        if stock.get("score") is not None
    ][:max_stocks]

    if not valid_stocks:
        lines.append("No stocks could be ranked.")
    else:
        for stock in valid_stocks:
            lines.extend([
                f"#{stock.get('rank', '-')} {stock.get('symbol', 'UNKNOWN')}",
                f"Score: {stock['score']}/100 | Rating: {stock.get('rating', 'N/A')}",
                "Reasons:"
            ])

            for reason in stock.get("reasons", []):
                lines.append(f"- {reason}")

            lines.append("")

    lines.extend([
        "Scores are rule-based and not validated predictions.",
        "Verify data and risk before making any trading decision."
    ])

    return "\n".join(lines)
