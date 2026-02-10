import json
import subprocess
import sys
from typing import List, Dict, Any


def _build_youtube_url(source_id: str) -> str:
    if source_id.startswith("PL"):
        return f"https://www.youtube.com/playlist?list={source_id}"
    return f"https://www.youtube.com/channel/{source_id}"


def fetch_ytdlp(channel_id: str) -> List[Dict[str, Any]]:
    channel_url = _build_youtube_url(channel_id)
    command = [
        sys.executable,
        "-m",
        "yt_dlp",
        "--dump-json",
        "--flat-playlist",
        "--playlist-end",
        "150",
        channel_url,
    ]
    result = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
    )
    items: List[Dict[str, Any]] = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            items.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return items
