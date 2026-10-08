from providers.data_normalizer import MarketDataNormalizer


def main():

    print("================================")
    print("RupAI Data Normalizer Test")
    print("================================")

    normalizer = MarketDataNormalizer()

    # Sample NSE-style recent data
    recent_data = {
        "priceInfo": {
            "lastPrice": 1300,
            "previousClose": 1280,
            "change": 20,
            "pChange": 1.56
        }
    }

    # Sample historical data
    historical_data = {
        "data": [
            {
                "date": "2026-07-14",
                "open": 1290,
                "high": 1310,
                "low": 1285,
                "close": 1300,
                "volume": 1000000,
                "turnover": 1300000000
            }
        ]
    }

    result = normalizer.normalize(
        "RELIANCE",
        recent_data,
        historical_data
    )

    print("\nNormalized data:")
    print(result)

    if (
        result["symbol"] == "RELIANCE"
        and result["recent"]["last_price"] == 1300
        and len(result["historical"]) == 1
    ):

        print("\n✅ NORMALIZER TEST SUCCESSFUL")

    else:

        print("\n❌ NORMALIZER TEST FAILED")


if __name__ == "__main__":
    main()
