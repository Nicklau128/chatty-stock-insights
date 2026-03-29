"""
OpenAI API client wrapper.

Encapsulates all communication with the OpenAI API. This abstraction
prevents direct dependency on the OpenAI SDK throughout the codebase
and enables easy mocking during testing.

Responsibilities:
- Send prompts to OpenAI models
- Return structured responses
- Handle API errors and retries

All LLM interactions should pass through this client.
"""

# Wrapper around OpenAI API

# integrations/openai_client.py

from openai import OpenAI
from .retry import retry_with_backoff
from .rate_limiter import RateLimiter


class OpenAIClient:

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.rate_limiter = RateLimiter(calls_per_minute=60)

    def chat(self, messages, model="gpt-4o-mini"):

        def _call():
            self.rate_limiter.wait()

            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
            )

            return response.choices[0].message.content

        return retry_with_backoff(_call)
