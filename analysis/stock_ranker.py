
from analysis.stock_scorer import score_stock


def rank_stocks(analysis_results):
    """
    Rank successfully analyzed stocks by score.
    Stocks without a valid score are kept at the bottom.
    """

    ranked = []

    for result in analysis_results:
        score_result = score_stock(result)
        ranked.append(score_result)

    ranked.sort(
        key=lambda item: (
            item["score"] is None,
            -(item["score"] or 0)
        )
    )

    for rank, item in enumerate(ranked, start=1):
        item["rank"] = rank

    return ranked
