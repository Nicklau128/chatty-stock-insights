"""Module to test OpenAIClient correctly retrieves and handles JSON
- Mocking an API to mimick OpenAI
- verfifies JSON output is valid and follows schema
"""

import json
from unittest.mock import MagicMock, patch

from app.integrations.openai_client import OpenAIClient


def test_openai_client_parses_json_response():
    fake_response = MagicMock()
    fake_response.choices = [MagicMock(message=MagicMock(content='{"intent":"analyze_trend","tickers":["AAPL"],"confidence":0.95}'))]

    fake_chat = MagicMock()
    fake_chat.completions.create.return_value = fake_response

    fake_openai = MagicMock(chat=fake_chat)

    with patch("app.integrations.openai_client.OpenAI", return_value=fake_openai):
        client = OpenAIClient(api_key="test")
        output = client.chat(messages=[{"role":"user","content":"Analyze AAPL"}], model="gpt-4o-mini")

    assert isinstance(output, str)
    parsed = json.loads(output)
    assert parsed["intent"] == "analyze_trend"
    assert parsed["tickers"] == ["AAPL"]
    assert parsed["confidence"] == 0.95
