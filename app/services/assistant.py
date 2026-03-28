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

import intent_service, finance_service

intent = intent_service.parse(query)
data = finance_service.fetch(intent)
# also add a summary generator service
