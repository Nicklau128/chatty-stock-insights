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

# finance_service.py

from datetime import datetime
from typing import List

from domain.models import (
    MarketData,
    Insight,
    InsightType,
    SignalType,
)
from domain.exceptions import DataUnavailableException
from integrations import StockProvider


# =====================================================
# DATA PROVIDER (Mock Implementation)
# =====================================================

class MarketDataProvider:

    def get_market_data(self, ticker: str) -> MarketData:

        if ticker.upper() == "UNKNOWN":
            raise DataUnavailableException(ticker)

        return MarketData(
            ticker=ticker.upper(),
            price=100.0,
            change_percent=1.25,
            volume=1_000_000,
            timestamp=datetime.utcnow(),
        )


# =====================================================
# FINANCE SERVICE
# =====================================================

class FinanceService:

    def __init__(self, stock_provider: StockProvider):
        self.stock_provider = stock_provider

    def get_stock_price(self, symbol:str) -> float:
        return self.stock_provider.get_price(symbol)

    # -----------------------------
    # Stock Summary
    # -----------------------------
    def get_stock_summary(self, ticker: str) -> Insight:

        data = self.stock_provider.get_price(ticker)

        summary = (
            f"{data.ticker} trades at {data.price:.2f}, "
            f"changing {data.change_percent:.2f}% today."
        )

        return Insight(
            ticker=data.ticker,
            insight_type=InsightType.VALUATION,
            summary=summary,
            confidence=0.9,
        )

    # -----------------------------
    # Trend Analysis
    # -----------------------------
    def analyze_trend(self, ticker: str) -> Insight:

        data = self.provider.get_market_data(ticker)

        if data.change_percent > 1:
            summary = "Upward momentum detected."
        elif data.change_percent < -1:
            summary = "Downward pressure observed."
        else:
            summary = "Price movement is stable."

        return Insight(
            ticker=data.ticker,
            insight_type=InsightType.TREND,
            summary=summary,
            confidence=0.7,
        )

    # -----------------------------
    # Price Movement Explanation
    # -----------------------------
    def explain_price_move(self, ticker: str) -> Insight:

        data = self.provider.get_market_data(ticker)

        direction = "up" if data.change_percent > 0 else "down"

        summary = (
            f"{data.ticker} moved {direction} "
            f"{abs(data.change_percent):.2f}% today, "
            "likely due to market sentiment or news catalysts."
        )

        return Insight(
            ticker=data.ticker,
            insight_type=InsightType.NEWS_IMPACT,
            summary=summary,
            confidence=0.5,
        )

    # -----------------------------
    # Comparison
    # -----------------------------
    def compare_assets(self, tickers: List[str]) -> Insight:

        data = [self.provider.get_market_data(t) for t in tickers]

        best = max(data, key=lambda x: x.change_percent)

        summary = (
            f"{best.ticker} shows strongest momentum "
            f"({best.change_percent:.2f}%)."
        )

        return Insight(
            ticker=best.ticker,
            insight_type=InsightType.MOMENTUM,
            summary=summary,
            confidence=0.75,
        )
