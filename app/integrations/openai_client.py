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
