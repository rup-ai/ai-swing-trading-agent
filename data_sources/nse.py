# RupAI Market Intelligence
# NSE data source layer

class NSEDataSource:
    """
    NSE market-data connector.

    This module is intentionally kept separate from the rest
    of the agent so the data provider can be changed later
    without rewriting the analysis engine.
    """

    def __init__(self):
        self.name = "NSE"

    def get_stock_data(self, symbol):
        """
        Placeholder for validated NSE/free market-data provider.

        Returns:
            dict containing market data for a stock.
        """

        return {
            "symbol": symbol,
            "source": self.name,
            "status": "not_connected"
        }

    def get_market_universe(self):
        """
        Placeholder for the complete eligible stock universe.
        """

        return {
            "source": self.name,
            "status": "not_connected",
            "stocks": []
        }
