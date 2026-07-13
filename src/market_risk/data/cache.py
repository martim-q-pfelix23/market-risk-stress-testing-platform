"""Local cache utilities for historical market data."""

from contextlib import suppress
import hashlib
import json
from pathlib import Path
from typing import Protocol
from uuid import uuid4

import pandas as pd

from market_risk.data.exceptions import MarketDataCacheError
from market_risk.data.models import MarketDataRequest

CACHE_FORMAT_VERSION = 1


def create_cache_key(request: MarketDataRequest) -> str:
    """Create a deterministic cache key for a market data request.

    Args:
        request: Validated historical market data request.

    Returns:
        A stable hexadecimal identifier representing the request.
    """
    payload = {
        "cache_format_version": CACHE_FORMAT_VERSION,
        "tickers": request.tickers,
        "start_date": request.start_date.isoformat(),
        "end_date": request.end_date.isoformat(),
    }

    serialised_payload = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
    )

    return hashlib.sha256(serialised_payload.encode("utf-8")).hexdigest()


class MarketDataCache(Protocol):
    """Define the contract for historical market data caches."""

    def load(
        self,
        request: MarketDataRequest,
    ) -> pd.DataFrame | None:
        """Load cached market data, returning None when it does not exist."""
        ...

    def save(
        self,
        request: MarketDataRequest,
        data: pd.DataFrame,
    ) -> None:
        """Store market data for a validated request."""
        ...


class ParquetMarketDataCache:
    """Store historical market data in local Parquet files."""

    def __init__(self, directory: Path) -> None:
        """Initialise the cache with its storage directory.

        Args:
            directory: Directory in which Parquet files will be stored.
        """
        self._directory = directory

    def load(
        self,
        request: MarketDataRequest,
    ) -> pd.DataFrame | None:
        """Load market data from the local cache.

        Args:
            request: Request used to identify the cached data.

        Returns:
            The cached DataFrame or None when no cached file exists.

        Raises:
            MarketDataCacheError: If the cached file cannot be read or does
                not satisfy the expected data contract.
        """
        cache_path = self._path_for(request)

        if not cache_path.is_file():
            return None

        try:
            data = pd.read_parquet(
                cache_path,
                engine="pyarrow",
                to_pandas_kwargs={},
            )
        except Exception as error:
            raise MarketDataCacheError(
                f"Failed to read cached market data: {cache_path.name}."
            ) from error

        self._validate_data(data, request)

        return data

    def save(
        self,
        request: MarketDataRequest,
        data: pd.DataFrame,
    ) -> None:
        """Store market data in the local cache.

        The data is first written to a temporary file and then moved to its
        final location. This prevents a partially written final cache file
        from being exposed if the write operation fails.

        Args:
            request: Request used to identify the cached data.
            data: Validated market data to store.

        Raises:
            MarketDataCacheError: If the data is invalid or cannot be written.
        """
        self._validate_data(data, request)

        cache_path = self._path_for(request)
        temporary_path = cache_path.with_name(f".{cache_path.name}.{uuid4().hex}.tmp")

        try:
            self._directory.mkdir(
                parents=True,
                exist_ok=True,
            )

            data.to_parquet(
                temporary_path,
                engine="pyarrow",
                compression="snappy",
                index=True,
            )

            temporary_path.replace(cache_path)
        except Exception as error:
            with suppress(OSError):
                temporary_path.unlink(missing_ok=True)

            raise MarketDataCacheError(
                f"Failed to write cached market data: {cache_path.name}."
            ) from error

    def _path_for(
        self,
        request: MarketDataRequest,
    ) -> Path:
        """Return the cache file path associated with a request."""
        cache_key = create_cache_key(request)
        return self._directory / f"{cache_key}.parquet"

    @staticmethod
    def _validate_data(
        data: pd.DataFrame,
        request: MarketDataRequest,
    ) -> None:
        """Validate data before it enters or leaves the cache."""
        if data.empty:
            raise MarketDataCacheError("Cached market data cannot be empty.")

        if not isinstance(data.index, pd.DatetimeIndex):
            raise MarketDataCacheError("Cached market data must use a DatetimeIndex.")

        if data.index.has_duplicates:
            raise MarketDataCacheError("Cached market data contains duplicated dates.")

        if not data.index.is_monotonic_increasing:
            raise MarketDataCacheError(
                "Cached market data must be ordered chronologically."
            )

        if data.index.tz is not None:
            raise MarketDataCacheError(
                "Cached market data must use a timezone-naive index."
            )

        actual_tickers = tuple(str(column).strip().upper() for column in data.columns)

        if actual_tickers != request.tickers:
            raise MarketDataCacheError(
                "Cached market data does not match the requested tickers."
            )

        if any(not pd.api.types.is_numeric_dtype(dtype) for dtype in data.dtypes):
            raise MarketDataCacheError("Cached market prices must be numeric.")

        if data.isna().all(axis="index").any():
            raise MarketDataCacheError(
                "Cached market data contains an unavailable ticker."
            )
