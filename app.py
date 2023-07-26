import streamlit as st
from streamlit.connections import ExperimentalBaseConnection
from streamlit.runtime.caching import cache_data
import openai

class OpenAIConnection(ExperimentalBaseConnection):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.total_tokens = 0

    def get_token_count(self):
        return self.total_tokens

    def _connect(self, **kwargs):
        if "api_key" in kwargs:
            api_key = kwargs.pop("api_key")
        else:
            api_key = st.secrets["openai_api_key"]
        openai.api_key = api_key
        return openai

    def query(
        self, query: str, engine: str = "gpt-3.5-turbo", ttl: int = 3600, **kwargs
    ) -> dict:
        @cache_data(ttl=ttl)
        def _query(query: str, engine: str, **kwargs) -> dict:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": query},
                ],
            )
            self.total_tokens += response["usage"]["total_tokens"]
            return response

        return _query(query, engine, **kwargs)
