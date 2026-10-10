
from analysis.stock_ranker import rank_stocks


def make_stock(symbol, close, sma20, sma50, rsi, trend):
    return {
        "symbol": symbol,
        "status": "SUCCESS",
        "indicators": {
            "latest_close": close,
            "sma_20": sma20,
            "sma_50": sma50,
            "rsi_14": rsi
        },
        "analysis": {
            "trend": trend,
            "momentum": "NEUTRAL"
        }
    }


def main():
    stocks = [
        make_stock("STOCK_A", 120, 110, 100, 60, "UPTREND"),
        make_stock("STOCK_B", 90, 100, 110, 40, "DOWNTREND"),
        make_stock("STOCK_C", 105, 100, 95, 55, "MIXED"),
        {
            "symbol": "STOCK_D",
            "status": "ANALYSIS_FAILED"
        }
    ]

    ranked = rank_stocks(stocks)

    print("Ranked stocks:")
    for stock in ranked:
        print(stock)

    assert len(ranked) == 4
    assert ranked[0]["symbol"] == "STOCK_A"
    assert ranked[-1]["score"] is None
    assert [item["rank"] for item in ranked] == [1, 2, 3, 4]

    print("\nPASS: Stock ranking test completed.")


if __name__ == "__main__":
    main()
