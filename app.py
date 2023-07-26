import streamlit as st
from streamlit.connections import ExperimentalBaseConnection
from openai_connection.connection import OpenAIConnection


conn = st.experimental_connection("openai", type=OpenAIConnection)

st.write(conn.query("Hello, how are you?"))
