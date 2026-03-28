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

class StockQuote(BaseModel):
    ticker: str
    price: float