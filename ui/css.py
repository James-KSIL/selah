import streamlit as st


def inject_css() -> None:
    css = """
        <style>
        @import url("https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600&display=swap");
        #MainMenu {visibility: hidden;}
        header [data-testid="stDecoration"] {display: none;}
        footer {visibility: hidden;}
        .stApp {
            padding-top: 0rem;
            background-color: #0B0F14;
            color: #E6E8EC;
        }
        .block-container {
            max-width: 1400px;
            margin: 0 auto;
            padding-top: 3rem;
        }
        [data-testid="stSidebar"] {
            background-color: #0C1117;
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }
        img {
            border-radius: 14px 14px 0 0;
            width: 100%;
            height: auto;
            object-fit: cover;
            aspect-ratio: 16 / 9;
            transition: transform 120ms ease, filter 120ms ease;
        }
        * {
            -webkit-user-select: none;
            user-select: none;
        }
        div[data-testid="stHorizontalBlock"] {
            flex-wrap: wrap;
            gap: 24px;
        }
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
            background: #11161D;
            border-radius: 14px;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
            overflow: hidden;
            padding: 0 0 0.65rem;
            flex: 1 1 50%;
        }
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:hover img {
            transform: scale(1.02);
            filter: brightness(1.05);
        }
        div[data-testid="stHorizontalBlock"] .video-title {
            margin: 0.6rem 0.85rem 0.25rem;
            font-weight: 600;
            line-height: 1.35;
            display: -webkit-box;
            -webkit-box-orient: vertical;
            -webkit-line-clamp: 2;
            overflow: hidden;
        }
        div[data-testid="stHorizontalBlock"] .video-meta {
            margin: 0 0.85rem 0.65rem;
            opacity: 0.65;
            font-size: 0.85rem;
        }
        div[data-testid="stHorizontalBlock"] button {
            margin: 0 0.85rem;
            padding: 0.35rem 0.6rem;
            font-size: 0.8rem;
            color: #CBD5E1;
            background: #1A2028;
            border: 1px solid rgba(255, 255, 255, 0.08);
        }
        @media (min-width: 900px) {
            div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
                flex: 1 1 33.333%;
            }
        }
        .selah-verse {
            margin-top: 1rem;
            padding: 0.75rem 0.9rem;
            border-radius: 12px;
            color: #f8f1d1;
            background: rgba(255, 255, 255, 0.02);
            opacity: 0.75;
            line-height: 1.5;
        .selah-logo {
            display: block;
            width: min(210px, 80%);
            height: auto;
            margin: 0.25rem auto 1rem;
            filter: brightness(0) invert(1);
        }
            text-shadow: none;
            animation: none;
        }
        .selah-verse .selah-ref {
            display: block;
            margin-top: 0.6rem;
            font-size: 0.85rem;
            opacity: 0.75;
        }
        [data-testid="stDeployButton"] {
            display: none;
        }
        [data-testid="stAppDeployButton"],
        .stAppDeployButton {
            display: none;
        }
        .selah-footer {
            margin: 1.25rem 0 0.5rem;
            padding: 0.65rem 0.8rem;
            border-radius: 10px;
            font-family: "Cinzel", "Georgia", serif;
            font-size: 0.85rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: #f5f5f5;
            background: rgba(255, 255, 255, 0.02);
            text-shadow: 0 1px 0 rgba(0, 0, 0, 0.6), 0 -1px 0 rgba(255, 255, 255, 0.08);
        }
        .selah-title {
            margin: 0.5rem 0 1rem;
            font-family: "Beautiful", "Cinzel", "Georgia", serif;
            font-size: 2.1rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: #F2F4F7;
        }
        </style>
        """
    st.markdown(
        css,
        unsafe_allow_html=True,
    )
