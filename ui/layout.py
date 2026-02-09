import base64
import os
from typing import Dict, List

import streamlit as st

from models.video_item import VideoItem
from ui.video_grid import render_video_grid


def select_channel(channels: Dict[str, str]) -> str:
    logo_path = os.path.join(
        os.path.dirname(__file__),
        "Screenshot_2026-02-09_005413-removebg-preview.png",
    )
    try:
        with open(logo_path, "rb") as logo_file:
            encoded = base64.b64encode(logo_file.read()).decode("ascii")
        st.sidebar.markdown(
            f"""
            <img class="selah-logo" src="data:image/png;base64,{encoded}" alt="Selah" />
            """,
            unsafe_allow_html=True,
        )
    except OSError:
        pass
    if not channels:
        st.sidebar.warning("No channels configured.")
        return ""
    channel_names = list(channels.keys())
    selected_name = st.sidebar.selectbox("Channel", channel_names)
    return channels[selected_name]


def render_layout(videos: List[VideoItem]) -> None:
    query = st.sidebar.text_input("Search", value="")
    focus_mode = st.sidebar.toggle("Focus Mode", value=False)
    st.sidebar.markdown(
        """
        <div class="selah-verse">
        Strength and honour are her clothing; and she shall rejoice in time to come.
        She openeth her mouth with wisdom; and in her tongue is the law of kindness.
        She looketh well to the ways of her household, and eateth not the bread of idleness.
        Her children arise up, and call her blessed; her husband also, and he praiseth her.
        Many daughters have done virtuously, but thou excellest them all.
        Favour is deceitful, and beauty is vain: but a woman that feareth the LORD, she shall be praised.
        <span class="selah-ref">Proverbs 31:25-30</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.markdown(
        """
        <div class="selah-footer">
        Created, Curated, and Crafted by KSIL
        </div>
        """,
        unsafe_allow_html=True,
    )

    filtered_videos = _filter_videos(videos, query)
    selected_video_id = st.session_state.get("selected_video_id")

    if focus_mode and selected_video_id:
        st.markdown(
            """
            <style>
            div[data-testid="stVideo"] iframe {
                height: 100vh !important;
            }
            div[data-testid="stVideo"] {
                height: 100vh !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        focused_video = _find_video(filtered_videos, selected_video_id)
        if focused_video and focused_video.embed_url:
            st.video(focused_video.embed_url)
            if focused_video.title:
                st.caption(focused_video.title)
            if st.button("Exit Focus Mode", key="exit_focus"):
                st.session_state["selected_video_id"] = None
        else:
            st.session_state["selected_video_id"] = None
    else:
        selected_video_id = render_video_grid(filtered_videos)
        if selected_video_id:
            st.session_state["selected_video_id"] = selected_video_id


def _filter_videos(videos: List[VideoItem], query: str) -> List[VideoItem]:
    if not query:
        return videos
    needle = query.lower()
    filtered: List[VideoItem] = []
    for video in videos:
        title = video.title or ""
        channel_name = video.channel_name or ""
        if needle in title.lower() or needle in channel_name.lower():
            filtered.append(video)
    return filtered


def _find_video(videos: List[VideoItem], video_id: str) -> VideoItem | None:
    for video in videos:
        if video.video_id == video_id:
            return video
    return None
