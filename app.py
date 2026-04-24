import streamlit as st
from agent.agent import Agent

# Page config
st.set_page_config(
    page_title="AI Payment Agent",
    page_icon="💳",
    layout="centered"
)

# Initialize session state
if "agent" not in st.session_state:
    st.session_state.agent = Agent(debug=False)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Header
st.title("💳 AI Payment Collection Agent")
st.caption("Secure • Intelligent • Conversational")

# Reset button
if st.button("🔄 Reset Session"):
    st.session_state.agent = Agent(debug=False)
    st.session_state.messages = []
    st.rerun()

st.divider()

# Chat display
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input
user_input = st.chat_input("Type your message...")

if user_input:
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Get response
    response = st.session_state.agent.next(user_input)
    bot_reply = response["message"]

    # Add agent message
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_reply
    })

    with st.chat_message("assistant"):
        st.markdown(bot_reply)