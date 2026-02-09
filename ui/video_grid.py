from typing import List, Optional

import html

import streamlit as st

from models.video_item import VideoItem


def render_video_grid(videos: List[VideoItem]) -> Optional[str]:
    selected_video_id = st.session_state.get("selected_video_id")
    columns = 3
    cols = st.columns(columns)

    for idx, video in enumerate(videos):
        col = cols[idx % columns]
        with col:
            media_slot = st.empty()
            if selected_video_id == video.video_id and video.embed_url:
                media_slot.video(video.embed_url)
            elif video.thumbnail:
                media_slot.image(video.thumbnail, width="stretch")
            if video.title:
                st.markdown(
                    f"<div class=\"video-title\">{html.escape(video.title)}</div>",
                    unsafe_allow_html=True,
                )
            if video.channel_name:
                st.markdown(
                    f"<div class=\"video-meta\">{html.escape(video.channel_name)}</div>",
                    unsafe_allow_html=True,
                )
            play_clicked = st.button(
                "Play",
                key=f"play_{video.video_id or idx}",
            )
            if play_clicked:
                selected_video_id = video.video_id
                st.session_state["selected_video_id"] = selected_video_id
                if video.embed_url:
                    media_slot.video(video.embed_url)
    return selected_video_id

