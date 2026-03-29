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

import requests
from integrations.retry import retry_with_backoff


class StockProvider:

    BASE_URL = "https://query1.finance.yahoo.com/v7/finance/quote"

    def get_price(self, symbol: str) -> float:

        def _call():
            response = requests.get(
                self.BASE_URL,
                params={"symbols": symbol},
                timeout=5,
            )

            response.raise_for_status()
            data = response.json()

            return data["quoteResponse"]["result"][0]["regularMarketPrice"]

        return retry_with_backoff(_call)
