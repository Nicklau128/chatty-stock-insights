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