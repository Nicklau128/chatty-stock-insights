"""
Intent interpretation service.

Responsible for converting natural language user queries into
structured query intents using an LLM.

Responsibilities:
- Call OpenAI to interpret queries
- Enforce structured output schemas
- Validate and parse AI responses
- Handle malformed or ambiguous outputs

This service isolates AI reasoning from application orchestration.
"""

# Calling Open AI
# parsing structured output
# validating schema

# intent_service.py

import json
from domain.intents import (
    Intent,
    IntentType,
    IntentFactory
)

from domain.exceptions import UnsupportedAnalysisException
from .finance_service import FinanceService
from integrations import OpenAIClient, StockProvider
from prompts.system_prompt import SYSTEM_PROMPT
from core.config import OPENAI_API_KEY


class IntentService:
    """
    Routes intents to domain services.
    """

    def __init__(self, llm_client: OpenAIClient):
        self.llm = llm_client or OpenAIClient(api_key=OPENAI_API_KEY)

        stock_provider = StockProvider()
        self.finance_service = FinanceService(stock_provider)

    # ---------------------------------

    def handle(self, intent: Intent):

        if intent.intent_type == IntentType.GET_STOCK_SUMMARY:
            return self.finance_service.get_stock_summary(
                intent.ticker
            )

        if intent.intent_type == IntentType.ANALYZE_TREND:
            return self.finance_service.analyze_trend(
                intent.ticker
            )

        if intent.intent_type == IntentType.COMPARE_ASSETS:
            return self.finance_service.compare_assets(
                intent.tickers
            )

        if intent.intent_type == IntentType.WHY_STOCK_MOVED:
            return self.finance_service.explain_price_move(
                intent.ticker
            )

        raise UnsupportedAnalysisException(intent.intent_type)

    def detect_intent(self, user_query: str) -> str:

        prompt = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query}
        ]

        text = self.llm.chat(messages=prompt, model="gpt-4o-mini")
        payload = json.loads(text)
        return IntentFactory.create(payload["intent"], ticker=payload.get("ticker"))
