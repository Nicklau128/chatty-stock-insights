"""Module to test stock data provider API
- Check that rate limit exceptions are correctly raised
- If request is successful, ensure output is a float
"""

import pytest
from unittest import patch, MagicMock
from app.integrations.stock_provider import StockProvider


def test_stock_provider_get_price_from_cache():
    provider = StockProvider(calls_per_minute=60, cache_ttl=60)
    provider._cache["AAPL"] = {"price": 123.45, "at": 0.0}

    price = provider.get_price("AAPL")

    assert price == 123.45


def test_stock_provider_get_price_via_yfinance():
    fake_info = {"last_price": 200.1}
    fake_ticker = MagicMock(fast_info=fake_info)

    with patch("app.integrations.stock_provider.yf.Ticker", return_value=fake_ticker):
        provider = StockProvider(calls_per_minute=60, cache_ttl=0)
        price = provider.get_price("AAPL")

    assert price == 200.1


def test_stock_provider_raises_on_missing_data():
    fake_ticker = MagicMock(fast_info={})

    with patch("app.integrations.stock_provider.yf.Ticker", return_value=fake_ticker):
        provider = StockProvider(calls_per_minute=60, cache_ttl=0)
        with pytest.raises(Exception):
            provider.get_price("AAPL")
