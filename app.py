import streamlit as st
import time
from chat_bot_logic import DsaChatbot

# Page configuration
st.set_page_config(
    page_title="DSA Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar
with st.sidebar:
    st.title("DSA Chatbot Settings")
    if st.button("💪 Motivation"):
        motivational_msg = st.session_state.chatbot.get_motivational()
        st.session_state.messages.append({"role": "assistant", "content": motivational_msg})
        # No rerun, just display below

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chatbot" not in st.session_state:
    st.session_state.chatbot = DsaChatbot()

if "first_run" not in st.session_state:
    st.session_state.first_run = True

# Display previous messages
for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]

    if role == "assistant":
        # Display entire content in a code block if it looks like code
        # You can comment out this next line if the content is normal text
        with st.chat_message("assistant"):
            st.code(content, language="python")
    else:
        with st.chat_message(role):
            st.markdown(content)

# First run greeting
if st.session_state.first_run:
    greeting = st.session_state.chatbot.get_greeting()
    st.session_state.messages.append({"role": "assistant", "content": greeting})
    with st.chat_message("assistant"):
        st.markdown(greeting)
    st.session_state.first_run = False

# Chat input at the bottom
user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get bot response
    if len(st.session_state.messages) > 2:
        response = st.session_state.chatbot.get_followup_response(user_input)
    else:
        response = st.session_state.chatbot.get_response(user_input)

    # Add assistant message
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Typing simulation without rerun
    with st.chat_message("assistant"):
        placeholder = st.empty()
        displayed_text = ""
        for char in response:
            displayed_text += char
            # Show everything as code block
            placeholder.code(displayed_text, language="python")
            time.sleep(0.01)
