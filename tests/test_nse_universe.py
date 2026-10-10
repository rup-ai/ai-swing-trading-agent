
from unittest.mock import Mock, patch

from data_sources.nse import NSEDataSource


def main():
    csv_text = (
        "SYMBOL,NAME OF COMPANY,SERIES\n"
        "AAA,Alpha Limited,EQ\n"
        "BBB,Beta Limited,EQ\n"
        "AAA,Alpha Limited,EQ\n"
    )

    with patch("data_sources.nse.requests.Session") as session_class:
        session = session_class.return_value
        response = Mock()
        response.text = csv_text
        response.raise_for_status.return_value = None
        session.get.return_value = response

        source = NSEDataSource()
        result = source.get_market_universe()

    print("NSE universe test result:")
    print(result)

    assert result["status"] == "success"
    assert result["count"] == 2
    assert [stock["symbol"] for stock in result["stocks"]] == [
        "AAA", "BBB"
    ]
    assert result["stocks"][0]["exchange"] == "NSE"

    print("\nPASS: NSE universe parsing test completed.")


if __name__ == "__main__":
    main()
