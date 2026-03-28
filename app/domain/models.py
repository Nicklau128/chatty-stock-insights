"""
Domain models used throughout the application.

These models represent structured business entities independent of
external APIs or frameworks. They define the internal data contracts
used between services.

Examples include:
- Stock quotes
- Comparison results
- Structured response payloads

Domain models should remain framework-agnostic and easily testable.
"""
from pydantic import BaseModel
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional

# class StockQuote(BaseModel):
#     ticker: str
#     price: float


# ======================
# ENUMS
# ======================

class AssetType(str, Enum):
    EQUITY = "equity"
    ETF = "etf"
    CRYPTO = "crypto"
    INDEX = "index"


class InsightType(str, Enum):
    TREND = "trend"
    VALUATION = "valuation"
    MOMENTUM = "momentum"
    RISK = "risk"
    NEWS_IMPACT = "news_impact"


class SignalType(str, Enum):
    BULLISH = "bullish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"


class Timeframe(str, Enum):
    DAY_1 = "1d"
    WEEK_1 = "1w"
    MONTH_1 = "1m"
    YEAR_1 = "1y"
    MAX = "max"


# ======================
# CORE MARKET MODELS
# ======================

@dataclass
class Asset:
    ticker: str
    name: str
    asset_type: AssetType
    exchange: str
    currency: str


@dataclass
class MarketData:
    ticker: str
    price: float
    change_percent: float
    volume: float
    timestamp: datetime


@dataclass
class OHLC:
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float


@dataclass
class HistoricalData:
    ticker: str
    timeframe: Timeframe
    prices: List[OHLC]


# ======================
# INSIGHT LAYER
# ======================

@dataclass
class Insight:
    ticker: str
    insight_type: InsightType
    summary: str
    confidence: float
    generated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Signal:
    ticker: str
    signal_type: SignalType
    strength: float
    reason: str


# ======================
# USER CONTEXT
# ======================

@dataclass
class Holding:
    ticker: str
    quantity: float
    avg_cost: float


@dataclass
class UserPortfolio:
    holdings: List[Holding] = field(default_factory=list)


@dataclass
class UserPreference:
    risk_level: Optional[str] = None
    horizon: Optional[str] = None
    preferred_assets: List[str] = field(default_factory=list)


# ======================
# CONVERSATION STATE
# ======================

@dataclass
class ConversationState:
    active_ticker: Optional[str] = None
    last_intent: Optional[str] = None
    pending_clarification: bool = False


# ======================
# SYSTEM STATUS
# ======================

@dataclass
class DataSourceStatus:
    provider: str
    available: bool
    latency_ms: int