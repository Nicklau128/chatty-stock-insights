# chatty-stock-insights
An LLM-powered app to answer your questions about the stock market today

## Instructions to run

1. Git clone `git clone chatty-stock-insights`
2. Navigate to root `cd chatty-stock-insights`
3. Create an environment configuration `.env` and specify your OpenAI API Key, see example in `.env.example`
4. Skip this if not running for the first time. If it is the first time running, first execute `docker compose build` to build images.
5. Run application with `docker compose up`.
6. Launch the web app with link `https://localhost:8501`

---

## Architecture overview

This application is designed in hexagonal layering that isolates core business logic from external dependencies, which optimises for maintainability and testability by enabling components to be updated without impacting the core logic.

[User]
|
v
[Streamlit UI]
|
v
[Assistant Service]
|
+-------------------
| |
v v
[IntentService] [FinanceService]
| |
+---> [OpenAI] +---> [StockProvider]
|
v
[Domain Models / Insight]
|
v
[Back to UI]

### Specific mappings of modules to their functions in the architecture

| Module | Functionality |
|--------|---------------|
| **streamlit_app.py** | UI entrypoint to input and send user queries |
| **assistant.py** | Core orchestration layer |
| **intent_service.py** | Routing user queries to Intents |
| **finance_service.py** | Logic for stock market data |
| **domain.models.py** | Internal data contracts between services |
| **domain.intents.py** | Structured representation of user intent
derived from natural language queries|
| **open_client.py** | OpenAI wrapper with retry and rate limit helpers |
| **config.py** | Load env variables incl API keys |


### Decisions and trade-offs

Key decisions
- Streamlit was chosen for rapid web UI prototyping, minimizing bolierplate code such as in Fast API.
- A central `assistant` service was used to coordinate intent parsing, data retrieval, and response generation, keeping workflow logic explicit
- While LLM was used to interpret user queries, business logic and data validation remained deterministic
- Containerised deployment to minimise dependency setup

Trade-offs
- Less demonstration of API design patterns compared to Fast API
- Synchronous workflow of the app may not be optimised for high concurrency or scaled usage

---

## Improvements

- Conversation memory can be introduced to allow implicit follow-up queries, e.g. "Is NVDA hitting a 52w high?" followed by "How does it compare to AMD?", the OpenAI client should be able to infer it refers to NVDA
- Adding an extra structured output validation for Intent service can help isolate errors caused by an output schema mismatch, which may occur due to LLM hallucinations despite the system prompt has been engineered to enforce an output schema.

---

## Prompt engineering to process user query

- Purpose is to classify an intent into given categories, not to infer an intent from zero-shot.
- system_prompt.py attempts to enforce a strict JSON output schema, and return a specifc selection of intents with an unknown fallback for queries with unclear intents. Three examples of user input and expected output are included in the prompt.
- Prioritisation handling when intents collide, e.g. "Why did Tesla drop more compared to Ford?" contains 2 intents of why_stock_moved and compare_assets, the order of importance is defined and only one will be chosen
- Only return tickers when their company names identifiable, ETFs are also included. Otherwise, an empty list will still be returned to maintain schema integrity.
- Save the confidence score alongside to be useful for services downstream.

---

## How AI helped build this app

- Developing architecture and repository structure for given requirements: Gemini and ChatGPT each presented a design of the app based on a summarised task definition, which resulted in a highly similar service partitioning strategy. ChatGPT's proposal was ultimately taken due to clear logic in setting the repo structure.
- Coding out the first iteration: following up on its design, ChatGPT wrote the first python drafts for classes implementation, along with doc strings to summarise the purposes of scripts.
- Debugging: This had been the largest productivity boost from AI. GitHub Copilot was employed to debug with a holistic view of the repository, ensuring modules are imported correctly, namings are consistent across services, investigate breaking points, etc.
- Accepting vs rejecting AI changes: Copilot was always paused before allowed to make direct edits or refactors, the decisions to keep or undo were reviewed on code-block basis file by file, carefully controlling large deltas against the original code.
