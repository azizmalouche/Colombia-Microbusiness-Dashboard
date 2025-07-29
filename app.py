import streamlit as st
import pandas as pd
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

# Load manual context
with open("dashboard_context.txt", "r", encoding="utf-8") as f:
    manual_context = f.read()

# UI setup
st.set_page_config(page_title="Dashboard Chatbot")
st.title("📊 Tableau Dashboard Chatbot")

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
prompt = st.chat_input("Ask something about the dashboard")

if prompt:
    # Add user message to session
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Construct full prompt with context and user question
    full_prompt = f"""
    You are a helpful analyst assistant. Use the data summary below to answer the user's question.

    Dashboard Description and Metric Definitions:
    {manual_context}

    User Question:
    {prompt}
    """

    # Call the model
    chat = ChatOllama(model="gemma:2b")
    response = chat.invoke(full_prompt).content

    # Add assistant response to session
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
