import streamlit as st

from services.ytdlp_fetcher import fetch_ytdlp


@st.cache_data(ttl=3600)
def fetch_ytdlp_cached(channel_id: str, fetch_method: str = "ytdlp"):
    return fetch_ytdlp(channel_id)
