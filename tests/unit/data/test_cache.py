"""Tests for market data cache utilities."""

from datetime import date
from pathlib import Path

import pandas as pd
import pytest

from market_risk.data.cache import (
    ParquetMarketDataCache,
    create_cache_key,
)
from market_risk.data.exceptions import MarketDataCacheError
from market_risk.data.models import MarketDataRequest


def create_request(
    tickers: tuple[str, ...] = ("AAPL", "MSFT"),
    start_date: date = date(2024, 1, 1),
    end_date: date = date(2024, 12, 31),
) -> MarketDataRequest:
    """Create a market data request for cache tests."""
    return MarketDataRequest(
        tickers=tickers,
        start_date=start_date,
        end_date=end_date,
    )


def create_market_data() -> pd.DataFrame:
    """Create valid deterministic market data for cache tests."""
    return pd.DataFrame(
        {
            "AAPL": [100.0, 102.0],
            "MSFT": [200.0, 204.0],
        },
        index=pd.DatetimeIndex(
            ["2024-01-02", "2024-01-03"],
            name="Date",
        ),
        dtype="float64",
    )


def test_create_deterministic_cache_key() -> None:
    """Generate the same key for equivalent requests."""
    first_request = create_request()
    second_request = create_request()

    assert create_cache_key(first_request) == create_cache_key(second_request)


def test_create_sha256_cache_key() -> None:
    """Return a valid hexadecimal SHA-256 identifier."""
    cache_key = create_cache_key(create_request())

    assert len(cache_key) == 64
    assert all(character in "0123456789abcdef" for character in cache_key)


def test_change_cache_key_when_tickers_change() -> None:
    """Generate a different key when the requested assets change."""
    first_key = create_cache_key(create_request())
    second_key = create_cache_key(
        create_request(tickers=("AAPL", "SPY")),
    )

    assert first_key != second_key


def test_change_cache_key_when_start_date_changes() -> None:
    """Generate a different key when the start date changes."""
    first_key = create_cache_key(create_request())
    second_key = create_cache_key(
        create_request(start_date=date(2023, 1, 1)),
    )

    assert first_key != second_key


def test_change_cache_key_when_end_date_changes() -> None:
    """Generate a different key when the end date changes."""
    first_key = create_cache_key(create_request())
    second_key = create_cache_key(
        create_request(end_date=date(2025, 1, 1)),
    )

    assert first_key != second_key


def test_return_none_when_cache_does_not_exist(
    tmp_path: Path,
) -> None:
    """Return None when no cached file exists for the request."""
    cache = ParquetMarketDataCache(tmp_path)

    result = cache.load(create_request())

    assert result is None


def test_save_and_load_market_data(
    tmp_path: Path,
) -> None:
    """Persist and recover market data without changing its contents."""
    cache = ParquetMarketDataCache(tmp_path)
    request = create_request()
    expected = create_market_data()

    cache.save(request, expected)
    result = cache.load(request)

    assert result is not None
    pd.testing.assert_frame_equal(result, expected)
    assert len(list(tmp_path.glob("*.parquet"))) == 1


def test_overwrite_existing_cache_entry(
    tmp_path: Path,
) -> None:
    """Replace an existing cache entry for the same request."""
    cache = ParquetMarketDataCache(tmp_path)
    request = create_request()
    original_data = create_market_data()
    updated_data = original_data * 2.0

    cache.save(request, original_data)
    cache.save(request, updated_data)

    result = cache.load(request)

    assert result is not None
    pd.testing.assert_frame_equal(result, updated_data)
    assert len(list(tmp_path.glob("*.parquet"))) == 1


def test_store_different_requests_separately(
    tmp_path: Path,
) -> None:
    """Use different files for different market data requests."""
    cache = ParquetMarketDataCache(tmp_path)

    first_request = create_request()
    first_data = create_market_data()

    second_request = create_request(
        tickers=("SPY",),
    )
    second_data = pd.DataFrame(
        {"SPY": [450.0, 455.0]},
        index=pd.DatetimeIndex(
            ["2024-01-02", "2024-01-03"],
            name="Date",
        ),
        dtype="float64",
    )

    cache.save(first_request, first_data)
    cache.save(second_request, second_data)

    first_result = cache.load(first_request)
    second_result = cache.load(second_request)

    assert first_result is not None
    assert second_result is not None
    pd.testing.assert_frame_equal(first_result, first_data)
    pd.testing.assert_frame_equal(second_result, second_data)
    assert len(list(tmp_path.glob("*.parquet"))) == 2


def test_reject_data_with_non_datetime_index(
    tmp_path: Path,
) -> None:
    """Reject invalid data before writing it to the cache."""
    cache = ParquetMarketDataCache(tmp_path)
    invalid_data = create_market_data()
    invalid_data.index = pd.Index(["2024-01-02", "2024-01-03"])

    with pytest.raises(
        MarketDataCacheError,
        match=r"Cached market data must use a DatetimeIndex\.",
    ):
        cache.save(
            create_request(),
            invalid_data,
        )

    assert not list(tmp_path.iterdir())


def test_reject_corrupted_cache_file(
    tmp_path: Path,
) -> None:
    """Translate Parquet read failures into a cache exception."""
    request = create_request()
    cache_key = create_cache_key(request)
    cache_path = tmp_path / f"{cache_key}.parquet"
    cache_path.write_text(
        "This is not a Parquet file.",
        encoding="utf-8",
    )

    cache = ParquetMarketDataCache(tmp_path)

    with pytest.raises(
        MarketDataCacheError,
        match=r"Failed to read cached market data: .+\.parquet\.",
    ) as exception_info:
        cache.load(request)

    assert exception_info.value.__cause__ is not None
