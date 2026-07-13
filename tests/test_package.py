"""Tests for the project package configuration."""

from importlib.metadata import version

import market_risk


def test_package_is_importable() -> None:
    """Verify that the core package can be imported."""
    assert market_risk.__doc__ is not None


def test_installed_package_version() -> None:
    """Verify that the installed package exposes the expected version."""
    assert version("market-risk-stress-testing-platform") == "0.1.0"
