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