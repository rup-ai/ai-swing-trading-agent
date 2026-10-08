from datetime import datetime


class MarketDataNormalizer:
    """
    Converts data from different market providers
    into one common structure for RupAI.
    """

    def normalize(self, symbol, recent_data=None, historical_data=None):

        result = {
            "symbol": symbol,
            "timestamp": datetime.utcnow().isoformat(),
            "recent": {},
            "historical": [],
        }

        # -----------------------------
        # Recent NSE data
        # -----------------------------

        if recent_data:

            price_info = recent_data.get("priceInfo", {})

            result["recent"] = {
                "last_price": price_info.get("lastPrice"),
                "previous_close": price_info.get("previousClose"),
                "change": price_info.get("change"),
                "change_percent": price_info.get(
                    "pChange"
                ),
            }

        # -----------------------------
        # Historical TejHQ data
        # -----------------------------

        if historical_data:

            rows = historical_data.get("data", [])

            for row in rows:

                result["historical"].append({
                    "date": row.get("date"),
                    "open": row.get("open"),
                    "high": row.get("high"),
                    "low": row.get("low"),
                    "close": row.get("close"),
                    "volume": row.get("volume"),
                    "turnover": row.get("turnover"),
                })

        return result
