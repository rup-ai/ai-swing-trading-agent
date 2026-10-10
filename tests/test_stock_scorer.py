
from analysis.stock_scorer import score_stock


def main():
    sample = {
        "symbol": "TESTSTOCK",
        "status": "SUCCESS",
        "indicators": {
            "latest_close": 120,
            "sma_20": 110,
            "sma_50": 100,
            "rsi_14": 60
        },
        "analysis": {
            "trend": "UPTREND",
            "momentum": "NEUTRAL"
        }
    }

    result = score_stock(sample)

    print("Scoring result:")
    print(result)

    assert result["symbol"] == "TESTSTOCK"
    assert result["score"] == 95
    assert result["rating"] == "HIGHER_RANKED"

    invalid = score_stock({
        "symbol": "BADSTOCK",
        "status": "ANALYSIS_FAILED"
    })

    assert invalid["score"] is None
    assert invalid["rating"] == "NOT_RANKED"

    print("\nPASS: Stock scoring tests completed.")


if __name__ == "__main__":
    main()
