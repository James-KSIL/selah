import streamlit as st

from config.channels import RSS_CHANNELS
from services.normalizer import normalize_ytdlp_entries, sort_video_items
from ui.css import inject_css
from ui.layout import render_layout, select_channel
from utils.cache import fetch_ytdlp_cached


def load_channels():
	return RSS_CHANNELS


def fetch_data(channel_id: str):
	if not channel_id:
		return []
	ytdlp_data = fetch_ytdlp_cached(channel_id)
	return ytdlp_data


def normalize_data(ytdlp_data):
	ytdlp_items = normalize_ytdlp_entries(ytdlp_data)
	return sort_video_items(ytdlp_items)


def main() -> None:
	st.set_page_config(layout="wide", initial_sidebar_state="expanded")

	inject_css()
	channels = load_channels()
	channel_id = select_channel(channels)
	ytdlp_data = fetch_data(channel_id)
	videos = normalize_data(ytdlp_data)
	render_layout(videos)


if __name__ == "__main__":
	main()
