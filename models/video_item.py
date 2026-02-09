from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class VideoItem:
    video_id: str
    title: str
    channel_name: str
    published: Optional[datetime]
    thumbnail: str
    duration: Optional[int]
    url: str
    embed_url: str
