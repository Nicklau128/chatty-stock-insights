"""
Stock data service.

Provides business-level access to stock market data by interacting
with external data providers and mapping raw API responses into
domain models.

Responsibilities:
- Retrieve stock quotes and metrics
- Normalize provider-specific responses
- Handle API failures and rate limits
- Provide clean data interfaces to the assistant service
"""

# Calling finance data provider yfinance/finnhub
# map raw API to domain models