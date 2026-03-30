"""
Streamlit user interface for the Stock Insights Assistant.

This module provides the presentation layer of the application.
It renders the web UI, captures user input, and displays assistant
responses. No business logic or external API calls should be
implemented here.

Responsibilities:
- Render input components and results
- Invoke the Assistant service
- Display formatted outputs to the user

The UI acts as a thin layer over the application services.
"""

import streamlit as st
from services.assistant import StockInsightsAssistant

assistant = StockInsightsAssistant()

st.title("Chatty Stock Insights")

query = st.text_input("Ask a question")

if st.button("Ask"):
    response = assistant.ask(query)
    st.write(response)