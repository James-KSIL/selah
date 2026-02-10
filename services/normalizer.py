from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional

from dateutil import parser as date_parser

from models.video_item import VideoItem


def _build_urls(video_id: Optional[str]) -> Dict[str, Optional[str]]:
    if not video_id:
        return {"url": None, "embed_url": None}
    return {
        "url": None,
        "embed_url": f"https://www.youtube.com/embed/{video_id}?rel=0&modestbranding=1&playsinline=1",
    }


def _parse_datetime(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    try:
        return date_parser.parse(value)
    except (ValueError, TypeError):
        return None


def _parse_yyyymmdd(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y%m%d")
    except (ValueError, TypeError):
        return None


def _is_unavailable(entry: Dict[str, Any]) -> bool:
    title = (entry.get("title") or "").strip().lower()
    if title in {"[deleted video]", "[private video]"}:
        return True
    availability = (entry.get("availability") or "").strip().lower()
    return availability in {"private", "needs_auth", "unavailable"}


def normalize_ytdlp_entries(entries: Iterable[Dict[str, Any]]) -> List[VideoItem]:
    items: List[VideoItem] = []
    for entry in entries:
        if _is_unavailable(entry):
            continue
        video_id = entry.get("id")
        if not video_id:
            continue
        urls = _build_urls(video_id)
        published = _parse_yyyymmdd(entry.get("upload_date"))
        thumbnail = entry.get("thumbnail")
        if not thumbnail:
            thumbnails = entry.get("thumbnails") or []
            if isinstance(thumbnails, list) and thumbnails:
                thumbnail = thumbnails[-1].get("url")
        items.append(
            VideoItem(
                video_id=video_id,
                title=entry.get("title"),
                channel_name=entry.get("uploader") or entry.get("channel"),
                published=published,
                thumbnail=thumbnail,
                duration=entry.get("duration"),
                url=urls["url"],
                embed_url=urls["embed_url"],
            )
        )
    return _sort_items(items)


def _sort_items(items: List[VideoItem]) -> List[VideoItem]:
    def sort_key(item: VideoItem) -> datetime:
        if item.published is None:
            return datetime.min
        return item.published

    return sorted(items, key=sort_key, reverse=True)


def sort_video_items(items: Iterable[VideoItem]) -> List[VideoItem]:
    return _sort_items(list(items))
