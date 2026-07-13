"""Contracts for historical market data providers."""

from typing import Protocol

import pandas as pd

from market_risk.data.models import MarketDataRequest


class MarketDataProvider(Protocol):
    """Define the contract for historical market data providers."""

    def get_adjusted_close(
        self,
        request: MarketDataRequest,
    ) -> pd.DataFrame:
        """Return adjusted closing prices for the requested assets.

        The returned DataFrame must satisfy the following contract:

        - use a DatetimeIndex;
        - contain one column per requested ticker;
        - use uppercase ticker names as columns;
        - contain prices ordered chronologically;
        - contain no duplicated dates;
        - contain numeric adjusted closing prices.

        Args:
            request: Validated market data request.

        Returns:
            A DataFrame containing adjusted closing prices.
        """
        ...
