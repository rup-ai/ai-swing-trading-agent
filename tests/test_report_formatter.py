
from analysis.report_formatter import format_ranked_report


def main():
    sample_result = {
        "scanned": 3,
        "analyzed": 2,
        "failed": 1,
        "ranked_stocks": [
            {
                "rank": 1,
                "symbol": "TEST_A",
                "score": 85,
                "rating": "HIGHER_RANKED",
                "reasons": ["Price above 20-day SMA."]
            },
            {
                "rank": 2,
                "symbol": "TEST_B",
                "score": 65,
                "rating": "MODERATE",
                "reasons": ["RSI indicates positive momentum."]
            },
            {
                "rank": 3,
                "symbol": "TEST_C",
                "score": None,
                "rating": "NOT_RANKED",
                "reasons": ["Analysis data unavailable."]
            }
        ]
    }

    report = format_ranked_report(sample_result, max_stocks=10)

    print(report)

    assert "TEST_A" in report
    assert "TEST_B" in report
    assert "TEST_C" not in report
    assert "Stocks scanned: 3" in report
    assert "not a buy/sell recommendation" in report

    print("\nPASS: Report formatter test completed.")


if __name__ == "__main__":
    main()
