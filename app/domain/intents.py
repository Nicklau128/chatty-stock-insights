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

class QueryIntent(BaseModel):
    intent: str
    tickers: list[str]