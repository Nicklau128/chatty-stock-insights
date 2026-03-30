"""
Assistant orchestration service.

This module coordinates the end-to-end workflow of processing a
user query. It acts as the central application service responsible
for invoking intent parsing, retrieving stock data, and generating
AI-powered summaries.

Workflow:
1. Receive user query
2. Parse intent via AI service
3. Fetch relevant stock data
4. Generate summarized response

This layer contains business orchestration logic and should remain
independent of UI and framework concerns.
"""

# import intent_service, finance_service

# intent = intent_service.parse(query)
# data = finance_service.fetch(intent)
# also add a summary generator service

# assistant.py

from domain.intents import IntentFactory
from .intent_service import IntentService
from .finance_service import FinanceService
from domain.exceptions import DomainException
from integrations import OpenAIClient, StockProvider


class StockInsightsAssistant:
    """
    Main assistant orchestrator.
    """

    def __init__(self, api_key: str):

        llm = OpenAIClient(api_key)
        stocks = StockProvider()
        # self.intent_service = IntentService(llm)
        self.intent_service = IntentService(llm)
        # self.finance_service = FinanceService(stocks)

    # ---------------------------------

    def handle_request(self, intent_name: str, **kwargs):

        try:
            # 1️⃣ Build intent
            intent = IntentFactory.create(intent_name, **kwargs)

            # 2️⃣ Execute intent
            insight = self.intent_service.handle(intent)

            # 3️⃣ Return response
            return insight.summary

        except DomainException as e:
            return f"Assistant error: {str(e)}"

        except Exception:
            return "Unexpected system error."
        
    def handle_query(self, user_query: str):
        intent = self.intent_service.detect_intent(user_query)
        return self.intent_service.handle(intent)
