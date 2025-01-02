import streamlit as st
import random
import time
import json
import os
import requests
from dotenv import load_dotenv
load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL") or "http://localhost:8000"

# Streamed response
def response_generator(prompt):
    res = requests.get(f"{BACKEND_URL}/chat/?query={prompt}").json()
    for word in res.split():
        yield word + " "
        time.sleep(0.05)


st.title("Real state agent chat bot")

with st.chat_message("assistant"):
    st.write("Hi how I can help you today?")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator(prompt))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})