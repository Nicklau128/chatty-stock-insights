"""
External stock data provider integration.

Handles communication with third-party financial data APIs
(e.g., Finnhub, Alpha Vantage, or yfinance).

Responsibilities:
- Perform API requests
- Parse raw provider responses
- Return normalized data structures
- Manage provider-specific concerns such as authentication
  and rate limiting
"""

# integrations/stock_provider.py

import time
import yfinance as yf
from integrations.retry import retry_with_backoff
from integrations.rate_limiter import RateLimiter
from app.domain.exceptions import DataUnavailableException


class StockProvider:

    def __init__(self, calls_per_minute=30, cache_ttl=30):
        self.rate_limiter = RateLimiter(calls_per_minute=calls_per_minute)
        self._cache = {}
        self._ttl = cache_ttl

    def get_price(self, symbol: str) -> float:

        symbol = symbol.upper().strip()
        cached = self._cache.get(symbol)
        if cached and time.time() - cached["at"] < self._ttl:
            return cached["price"]

        self.rate_limiter.wait()

        def _call():
            ticker = yf.Ticker(symbol)
            info = getattr(ticker, "fast_info", None)
            if info is None:
                info = ticker.info

            price = (
                info.get("last_price")
                or info.get("regularMarketPrice")
                or info.get("currentPrice")
            )

            if price is None:
                raise DataUnavailableException(symbol)

            return price

        price = retry_with_backoff(
            _call,
            attempts=5,
            base_wait=1.0,
            max_wait=8.0,
        )

        self._cache[symbol] = {"price": price, "at": time.time()}
        return price
