"""
Query intent definitions.

This module defines the structured representation of user intent
derived from natural language queries. Intent objects act as the
contract between the AI interpretation layer and application
business logic.

Responsibilities:
- Define supported query types
- Represent extracted tickers and parameters
- Validate AI-generated intent data
"""

# Pure logic contracts 

# class QueryIntent(BaseModel):
#     intent: str
#     tickers: list[str]


# intents.py

from enum import Enum
from dataclasses import dataclass
from typing import List, Optional

from .models import Timeframe
from .exceptions import MissingParameterException


# ======================
# INTENT ENUM
# ======================

class IntentType(str, Enum):
    GET_STOCK_SUMMARY = "get_stock_summary"
    ANALYZE_TREND = "analyze_trend"
    COMPARE_ASSETS = "compare_assets"
    WHY_STOCK_MOVED = "why_stock_moved"
    MARKET_OVERVIEW = "market_overview"


# ======================
# BASE INTENT
# ======================

@dataclass
class Intent:
    intent_type: IntentType


# ======================
# SPECIFIC INTENTS
# ======================

@dataclass
class StockSummaryIntent(Intent):
    ticker: str


@dataclass
class AnalyzeTrendIntent(Intent):
    ticker: str
    timeframe: Timeframe = Timeframe.MONTH_1


@dataclass
class CompareAssetsIntent(Intent):
    tickers: List[str]
    timeframe: Timeframe = Timeframe.MONTH_1

    def validate(self):
        if len(self.tickers) < 2:
            raise MissingParameterException("at least two tickers")


@dataclass
class WhyStockMovedIntent(Intent):
    ticker: str


# ======================
# SIMPLE INTENT FACTORY
# ======================

class IntentFactory:
    """
    Converts structured inputs into domain intents.
    Later this connects to LLM/NLU output.
    """

    @staticmethod
    def create(intent_name: str, **kwargs) -> Intent:

        intent_type = IntentType(intent_name)

        if intent_type == IntentType.GET_STOCK_SUMMARY:
            return StockSummaryIntent(intent_type, kwargs["ticker"])

        if intent_type == IntentType.ANALYZE_TREND:
            return AnalyzeTrendIntent(
                intent_type,
                kwargs["ticker"],
                kwargs.get("timeframe", Timeframe.MONTH_1),
            )

        if intent_type == IntentType.COMPARE_ASSETS:
            intent = CompareAssetsIntent(
                intent_type,
                kwargs["tickers"],
                kwargs.get("timeframe", Timeframe.MONTH_1),
            )
            intent.validate()
            return intent

        if intent_type == IntentType.WHY_STOCK_MOVED:
            return WhyStockMovedIntent(intent_type, kwargs["ticker"])

        raise ValueError(f"Unknown intent: {intent_name}")
