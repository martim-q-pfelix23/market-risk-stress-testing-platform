"""Opt-in integration tests for the Yahoo Finance provider."""

import os
from datetime import date

import pandas as pd
import pytest

from market_risk.data.models import MarketDataRequest
from market_risk.data.yahoo import YahooFinanceProvider

NETWORK_TESTS_ENABLED = os.getenv("RUN_NETWORK_TESTS") == "1"


@pytest.mark.network
@pytest.mark.skipif(
    not NETWORK_TESTS_ENABLED,
    reason="Network tests require RUN_NETWORK_TESTS=1.",
)
def test_retrieve_live_adjusted_close_prices() -> None:
    """Retrieve and normalise historical prices from Yahoo Finance."""
    request = MarketDataRequest(
        tickers=("AAPL", "MSFT"),
        start_date=date(2024, 1, 2),
        end_date=date(2024, 1, 10),
    )
    provider = YahooFinanceProvider()

    result = provider.get_adjusted_close(request)

    assert not result.empty
    assert isinstance(result.index, pd.DatetimeIndex)
    assert result.index.is_monotonic_increasing
    assert not result.index.has_duplicates
    assert list(result.columns) == ["AAPL", "MSFT"]
    assert result.columns.name is None
    assert result.index.name == "Date"
    assert result.notna().any(axis="index").all()
    assert all(pd.api.types.is_float_dtype(dtype) for dtype in result.dtypes)
