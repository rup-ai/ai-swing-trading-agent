
from unittest.mock import patch

from data_collector import collect_market_data


def main():
    mock_data = {
        "AAA": {"data": [{"close": 100}]},
        "BBB": {"error": "Provider unavailable"},
        "CCC": {"data": []},
    }

    with (
        patch("data_collector.get_initial_universe",
              return_value=["AAA", "BBB", "CCC"]),
        patch("data_collector.MarketDataSource") as mock_source,
    ):
        mock_source.return_value.get_multiple_stocks.return_value = (
            mock_data
        )

        result = collect_market_data()

    assert result == mock_data
    assert len(result) == 3

    print("PASS: Collector preserves provider results.")


if __name__ == "__main__":
    main()
