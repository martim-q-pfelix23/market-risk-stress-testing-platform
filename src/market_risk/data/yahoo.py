"""Yahoo Finance adapter for historical market data."""

from collections.abc import Callable
from datetime import timedelta
from typing import cast

import pandas as pd
import yfinance as yf

from market_risk.data.exceptions import (
    MarketDataRetrievalError,
    MarketDataUnavailableError,
    MarketDataValidationError,
)
from market_risk.data.models import MarketDataRequest
from market_risk.data.provider import MarketDataProvider

DownloadFunction = Callable[..., pd.DataFrame | None]


class YahooFinanceProvider(MarketDataProvider):
    """Retrieve and normalise historical prices from Yahoo Finance."""

    def __init__(
        self,
        downloader: DownloadFunction | None = None,
    ) -> None:
        """Initialise the provider with an optional download function.

        Args:
            downloader: Function used to retrieve raw market data. When omitted,
                the provider uses ``yfinance.download``.
        """
        self._downloader = downloader or cast(DownloadFunction, yf.download)

    def get_adjusted_close(
        self,
        request: MarketDataRequest,
    ) -> pd.DataFrame:
        """Return validated adjusted closing prices.

        Args:
            request: Validated request containing tickers and date boundaries.

        Returns:
            A chronologically ordered DataFrame containing one column per ticker.

        Raises:
            MarketDataRetrievalError: If the external provider raises an error.
            MarketDataUnavailableError: If usable data cannot be found.
            MarketDataValidationError: If the returned data violates the
                internal market data contract.
        """
        raw_data = self._download_data(request)
        return self._normalise_close_prices(raw_data, request)

    def _download_data(
        self,
        request: MarketDataRequest,
    ) -> pd.DataFrame:
        """Download raw daily market data from Yahoo Finance."""
        inclusive_end_date = request.end_date + timedelta(days=1)

        try:
            raw_data = self._downloader(
                tickers=list(request.tickers),
                start=request.start_date,
                end=inclusive_end_date,
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
        except Exception as error:
            tickers = ", ".join(request.tickers)
            raise MarketDataRetrievalError(
                f"Failed to retrieve market data for: {tickers}."
            ) from error

        if raw_data is None or raw_data.empty:
            tickers = ", ".join(request.tickers)
            raise MarketDataUnavailableError(
                f"No market data is available for: {tickers}."
            )

        return raw_data

    @staticmethod
    def _normalise_close_prices(
        raw_data: pd.DataFrame,
        request: MarketDataRequest,
    ) -> pd.DataFrame:
        """Convert Yahoo Finance output into the internal price format."""
        if not isinstance(raw_data.index, pd.DatetimeIndex):
            raise MarketDataValidationError("Market data must use a DatetimeIndex.")

        if raw_data.index.has_duplicates:
            raise MarketDataValidationError("Market data contains duplicated dates.")

        if not isinstance(raw_data.columns, pd.MultiIndex):
            raise MarketDataValidationError(
                "Yahoo Finance data must use MultiIndex columns."
            )

        try:
            close_data = raw_data.xs(
                "Close",
                axis="columns",
                level=0,
            )
        except KeyError as error:
            raise MarketDataValidationError(
                "Yahoo Finance data does not contain adjusted closing prices."
            ) from error

        if isinstance(close_data, pd.Series):
            close_data = close_data.to_frame()

        close_data = close_data.copy()
        close_data.columns = pd.Index(
            str(column).strip().upper() for column in close_data.columns
        )

        if close_data.columns.has_duplicates:
            raise MarketDataValidationError(
                "Market data contains duplicated ticker columns."
            )

        missing_tickers = [
            ticker for ticker in request.tickers if ticker not in close_data.columns
        ]

        if missing_tickers:
            missing = ", ".join(missing_tickers)
            raise MarketDataUnavailableError(
                f"No market data was returned for: {missing}."
            )

        prices = close_data.loc[:, list(request.tickers)].copy()

        non_numeric_tickers = [
            ticker
            for ticker in request.tickers
            if not pd.api.types.is_numeric_dtype(prices[ticker].dtype)
        ]

        if non_numeric_tickers:
            invalid = ", ".join(non_numeric_tickers)
            raise MarketDataValidationError(
                f"Market prices must be numeric for: {invalid}."
            )

        unavailable_tickers = [
            ticker for ticker in request.tickers if prices[ticker].isna().all()
        ]

        if unavailable_tickers:
            unavailable = ", ".join(unavailable_tickers)
            raise MarketDataUnavailableError(
                f"No usable market data was returned for: {unavailable}."
            )

        prices = prices.dropna(how="all")

        if prices.empty:
            raise MarketDataUnavailableError(
                "No usable market data remains after validation."
            )

        normalised_index = pd.DatetimeIndex(prices.index)

        if normalised_index.tz is not None:
            normalised_index = normalised_index.tz_localize(None)

        prices.index = normalised_index

        start_timestamp = pd.Timestamp(request.start_date)
        end_timestamp = pd.Timestamp(request.end_date)

        prices = prices.loc[
            (prices.index >= start_timestamp) & (prices.index <= end_timestamp)
        ]

        if prices.empty:
            raise MarketDataUnavailableError(
                "No market data exists inside the requested date range."
            )

        prices = prices.sort_index()
        prices.index.name = "Date"
        prices.columns.name = None

        return prices.astype("float64")
