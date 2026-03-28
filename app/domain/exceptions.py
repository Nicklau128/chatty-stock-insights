"""
Custom application exceptions.

Defines domain-specific error types used across services to provide
consistent error handling and clearer failure semantics.

Examples:
- InvalidQueryError
- StockDataUnavailableError
- AIResponseParsingError

Using custom exceptions helps isolate infrastructure failures from
business logic concerns.
"""

# exceptions.py

class DomainException(Exception):
    """Base exception for domain errors."""
    pass


# ======================
# USER INPUT ERRORS
# ======================

class UnknownTickerException(DomainException):
    def __init__(self, ticker: str):
        super().__init__(f"Unknown ticker: {ticker}")
        self.ticker = ticker


class AmbiguousAssetException(DomainException):
    def __init__(self, query: str, candidates: list):
        message = f"Ambiguous asset '{query}'. Candidates: {candidates}"
        super().__init__(message)
        self.query = query
        self.candidates = candidates


class MissingParameterException(DomainException):
    def __init__(self, parameter: str):
        super().__init__(f"Missing required parameter: {parameter}")
        self.parameter = parameter


# ======================
# DATA ERRORS
# ======================

class DataUnavailableException(DomainException):
    def __init__(self, ticker: str):
        super().__init__(f"Data unavailable for {ticker}")
        self.ticker = ticker


class MarketClosedException(DomainException):
    def __init__(self):
        super().__init__("Market is currently closed.")


# ======================
# CAPABILITY ERRORS
# ======================

class UnsupportedAnalysisException(DomainException):
    def __init__(self, request: str):
        super().__init__(f"Unsupported analysis request: {request}")
        self.request = request


# ======================
# CONVERSATION ERRORS
# ======================

class LostContextException(DomainException):
    def __init__(self):
        super().__init__("Conversation context is unclear.")
