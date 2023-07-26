import streamlit as st
from openai_connection.connection import OpenAIConnection

with st.sidebar:
    openai_api_key = st.text_input(
        "OpenAI API Key", key="chatbot_api_key", type="password"
    )

st.title("💬 Chatbot Demo")
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How can I help you?"}
    ]

if openai_api_key:
    conn = st.experimental_connection(
        "openai", type=OpenAIConnection, api_key=openai_api_key
    )

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    st.chat_message("user").write(prompt)
    try:
        msg = conn.query(prompt, messages=st.session_state.messages).choices[0].message
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append(msg)
        st.chat_message("assistant").write(msg.content)
    except Exception as error:
        st.info(error)
        st.stop()
