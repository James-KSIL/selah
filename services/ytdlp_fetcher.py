import json
import subprocess
import sys
from typing import List, Dict, Any


def fetch_ytdlp(channel_id: str) -> List[Dict[str, Any]]:
    channel_url = f"https://www.youtube.com/channel/{channel_id}"
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
