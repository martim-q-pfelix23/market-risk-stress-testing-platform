"""Domain models for historical market data requests."""

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class MarketDataRequest:
    """Represent a validated request for historical market data.

    Attributes:
        tickers: Financial asset identifiers requested by the user.
        start_date: First date of the requested analysis period.
        end_date: Last date of the requested analysis period.
    """

    tickers: tuple[str, ...]
    start_date: date
    end_date: date

    def __post_init__(self) -> None:
        """Normalise and validate the request after initialisation."""
        normalised_tickers = tuple(ticker.strip().upper() for ticker in self.tickers)

        if not normalised_tickers:
            raise ValueError("At least one ticker must be provided.")

        if any(not ticker for ticker in normalised_tickers):
            raise ValueError("Tickers cannot be empty.")

        if len(normalised_tickers) > 20:
            raise ValueError("A maximum of 20 tickers is allowed.")

        if len(set(normalised_tickers)) != len(normalised_tickers):
            raise ValueError("Duplicate tickers are not allowed.")

        if self.start_date >= self.end_date:
            raise ValueError("The start date must be before the end date.")

        object.__setattr__(self, "tickers", normalised_tickers)
