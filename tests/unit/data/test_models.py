"""Tests for market data domain models."""

from dataclasses import FrozenInstanceError
from datetime import date

import pytest

from market_risk.data.models import MarketDataRequest


def test_create_valid_market_data_request() -> None:
    """Create a request with valid tickers and dates."""
    request = MarketDataRequest(
        tickers=("AAPL", "MSFT"),
        start_date=date(2020, 1, 1),
        end_date=date(2025, 1, 1),
    )

    assert request.tickers == ("AAPL", "MSFT")
    assert request.start_date == date(2020, 1, 1)
    assert request.end_date == date(2025, 1, 1)


def test_normalise_tickers() -> None:
    """Remove surrounding spaces and convert tickers to uppercase."""
    request = MarketDataRequest(
        tickers=(" aapl ", "msft"),
        start_date=date(2020, 1, 1),
        end_date=date(2025, 1, 1),
    )

    assert request.tickers == ("AAPL", "MSFT")


def test_reject_empty_ticker_collection() -> None:
    """Reject requests without any tickers."""
    with pytest.raises(
        ValueError,
        match=r"At least one ticker must be provided\.",
    ):
        MarketDataRequest(
            tickers=(),
            start_date=date(2020, 1, 1),
            end_date=date(2025, 1, 1),
        )


def test_reject_blank_ticker() -> None:
    """Reject tickers containing only whitespace."""
    with pytest.raises(
        ValueError,
        match=r"Tickers cannot be empty\.",
    ):
        MarketDataRequest(
            tickers=("AAPL", "   "),
            start_date=date(2020, 1, 1),
            end_date=date(2025, 1, 1),
        )


def test_reject_more_than_twenty_tickers() -> None:
    """Reject requests exceeding the supported portfolio size."""
    tickers = tuple(f"ASSET{i}" for i in range(21))

    with pytest.raises(
        ValueError,
        match=r"A maximum of 20 tickers is allowed\.",
    ):
        MarketDataRequest(
            tickers=tickers,
            start_date=date(2020, 1, 1),
            end_date=date(2025, 1, 1),
        )


def test_reject_duplicate_tickers_after_normalisation() -> None:
    """Reject duplicated tickers regardless of casing and spacing."""
    with pytest.raises(
        ValueError,
        match=r"Duplicate tickers are not allowed\.",
    ):
        MarketDataRequest(
            tickers=("AAPL", " aapl "),
            start_date=date(2020, 1, 1),
            end_date=date(2025, 1, 1),
        )


@pytest.mark.parametrize(
    ("start_date", "end_date"),
    [
        (date(2025, 1, 1), date(2025, 1, 1)),
        (date(2025, 1, 2), date(2025, 1, 1)),
    ],
)
def test_reject_invalid_date_range(
    start_date: date,
    end_date: date,
) -> None:
    """Reject equal or chronologically inverted dates."""
    with pytest.raises(
        ValueError,
        match=r"The start date must be before the end date\.",
    ):
        MarketDataRequest(
            tickers=("AAPL",),
            start_date=start_date,
            end_date=end_date,
        )


def test_market_data_request_is_immutable() -> None:
    """Prevent modification after the request has been created."""
    request = MarketDataRequest(
        tickers=("AAPL",),
        start_date=date(2020, 1, 1),
        end_date=date(2025, 1, 1),
    )

    with pytest.raises(FrozenInstanceError):
        request.tickers = ("MSFT",)
