"""Custom exceptions for the market data layer."""


class MarketDataError(Exception):
    """Base exception for all market data errors."""


class MarketDataRetrievalError(MarketDataError):
    """Raised when market data cannot be retrieved from an external provider."""


class MarketDataValidationError(MarketDataError):
    """Raised when retrieved market data violates the internal data contract."""


class MarketDataUnavailableError(MarketDataError):
    """Raised when no usable data is available for a requested asset."""
