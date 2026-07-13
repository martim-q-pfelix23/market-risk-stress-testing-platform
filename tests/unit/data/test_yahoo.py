"""Tests for the Yahoo Finance market data provider."""

from datetime import date, timedelta
from unittest.mock import Mock

import pandas as pd
import pytest

from market_risk.data.exceptions import (
    MarketDataRetrievalError,
    MarketDataUnavailableError,
    MarketDataValidationError,
)
from market_risk.data.models import MarketDataRequest
from market_risk.data.yahoo import YahooFinanceProvider


def create_request() -> MarketDataRequest:
    """Create a reusable valid market data request."""
    return MarketDataRequest(
        tickers=("AAPL", "MSFT"),
        start_date=date(2024, 1, 1),
        end_date=date(2024, 1, 3),
    )


def create_raw_market_data() -> pd.DataFrame:
    """Create representative Yahoo Finance MultiIndex data."""
    columns = pd.MultiIndex.from_tuples(
        [
            ("Close", "AAPL"),
            ("Close", "MSFT"),
            ("Open", "AAPL"),
            ("Open", "MSFT"),
        ],
        names=["Price", "Ticker"],
    )

    index = pd.DatetimeIndex(
        [
            "2024-01-03",
            "2024-01-02",
        ],
        name="Date",
    )

    return pd.DataFrame(
        [
            [102.0, 202.0, 101.0, 201.0],
            [100.0, 200.0, 99.0, 199.0],
        ],
        index=index,
        columns=columns,
    )


def test_return_normalised_adjusted_close_prices() -> None:
    """Return only requested close prices in chronological order."""
    raw_data = create_raw_market_data()
    downloader = Mock(return_value=raw_data)
    provider = YahooFinanceProvider(downloader=downloader)

    result = provider.get_adjusted_close(create_request())

    expected = pd.DataFrame(
        {
            "AAPL": [100.0, 102.0],
            "MSFT": [200.0, 202.0],
        },
        index=pd.DatetimeIndex(
            ["2024-01-02", "2024-01-03"],
            name="Date",
        ),
    )

    pd.testing.assert_frame_equal(result, expected)

    downloader.assert_called_once_with(
        tickers=["AAPL", "MSFT"],
        start=date(2024, 1, 1),
        end=date(2024, 1, 3) + timedelta(days=1),
        interval="1d",
        group_by="column",
        auto_adjust=True,
        actions=False,
        progress=False,
        threads=False,
        keepna=False,
        ignore_tz=True,
        multi_level_index=True,
    )


def test_convert_download_failure_to_domain_exception() -> None:
    """Convert external provider failures into an internal exception."""
    original_error = RuntimeError("Network unavailable.")
    downloader = Mock(side_effect=original_error)
    provider = YahooFinanceProvider(downloader=downloader)

    with pytest.raises(
        MarketDataRetrievalError,
        match=r"Failed to retrieve market data for: AAPL, MSFT\.",
    ) as exception_info:
        provider.get_adjusted_close(create_request())

    assert exception_info.value.__cause__ is original_error


def test_reject_empty_provider_response() -> None:
    """Reject an empty DataFrame returned by the provider."""
    downloader = Mock(return_value=pd.DataFrame())
    provider = YahooFinanceProvider(downloader=downloader)

    with pytest.raises(
        MarketDataUnavailableError,
        match=r"No market data is available for: AAPL, MSFT\.",
    ):
        provider.get_adjusted_close(create_request())


def test_reject_non_datetime_index() -> None:
    """Reject market data without a DatetimeIndex."""
    raw_data = create_raw_market_data()
    raw_data.index = pd.Index(["2024-01-03", "2024-01-02"])

    provider = YahooFinanceProvider(downloader=Mock(return_value=raw_data))

    with pytest.raises(
        MarketDataValidationError,
        match=r"Market data must use a DatetimeIndex\.",
    ):
        provider.get_adjusted_close(create_request())


def test_reject_duplicated_dates() -> None:
    """Reject market data containing duplicated dates."""
    raw_data = create_raw_market_data()
    raw_data.index = pd.DatetimeIndex(["2024-01-02", "2024-01-02"])

    provider = YahooFinanceProvider(downloader=Mock(return_value=raw_data))

    with pytest.raises(
        MarketDataValidationError,
        match=r"Market data contains duplicated dates\.",
    ):
        provider.get_adjusted_close(create_request())


def test_reject_missing_close_prices() -> None:
    """Reject responses without a Close field."""
    raw_data = create_raw_market_data()
    raw_data = raw_data.drop(columns="Close", level=0)

    provider = YahooFinanceProvider(downloader=Mock(return_value=raw_data))

    with pytest.raises(
        MarketDataValidationError,
        match=(
            r"Yahoo Finance data does not contain "
            r"adjusted closing prices\."
        ),
    ):
        provider.get_adjusted_close(create_request())


def test_reject_missing_requested_ticker() -> None:
    """Reject responses missing one of the requested assets."""
    raw_data = create_raw_market_data()
    raw_data = raw_data.drop(columns="MSFT", level=1)

    provider = YahooFinanceProvider(downloader=Mock(return_value=raw_data))

    with pytest.raises(
        MarketDataUnavailableError,
        match=r"No market data was returned for: MSFT\.",
    ):
        provider.get_adjusted_close(create_request())


def test_reject_non_numeric_prices() -> None:
    """Reject price columns containing non-numeric values."""
    raw_data = create_raw_market_data()
    raw_data[("Close", "AAPL")] = ["invalid", "invalid"]

    provider = YahooFinanceProvider(downloader=Mock(return_value=raw_data))

    with pytest.raises(
        MarketDataValidationError,
        match=r"Market prices must be numeric for: AAPL\.",
    ):
        provider.get_adjusted_close(create_request())


def test_reject_completely_unavailable_ticker() -> None:
    """Reject an asset whose price series contains only missing values."""
    raw_data = create_raw_market_data()
    raw_data[("Close", "MSFT")] = float("nan")

    provider = YahooFinanceProvider(downloader=Mock(return_value=raw_data))

    with pytest.raises(
        MarketDataUnavailableError,
        match=r"No usable market data was returned for: MSFT\.",
    ):
        provider.get_adjusted_close(create_request())
