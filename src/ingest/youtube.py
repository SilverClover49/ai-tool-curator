"""Parse YouTube watch history from Google Takeout exports."""

import json
import os
from pathlib import Path
from datetime import datetime


def parse_youtube_history(data_dir: str) -> list[dict]:
    """Parse YouTube watch history JSON files from Google Takeout."""
    entries = []
    data_path = Path(data_dir)

    for json_file in data_path.rglob("*watch-history*.json"):
        entries.extend(_parse_watch_file(json_file))

    for json_file in data_path.rglob("*youtube-history*.json"):
        entries.extend(_parse_watch_file(json_file))

    entries.sort(key=lambda x: x.get("date", ""), reverse=True)
    return entries


def _parse_watch_file(filepath: Path) -> list[dict]:
    """Parse a single YouTube watch history file."""
    entries = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return entries

    for item in data:
        title = item.get("title", "")
        url = item.get("titleUrl", "")
        subtitles = item.get("subtitles", [])
        time_str = item.get("time", "")

        channel = ""
        if subtitles:
            channel = subtitles[0].get("name", "")

        description = ""
        if subtitles:
            description = f"Channel: {channel}"

        parsed_date = ""
        if time_str:
            try:
                dt = datetime.fromisoformat(time_str.replace("Z", "+00:00"))
                parsed_date = dt.strftime("%Y-%m-%d")
            except (ValueError, TypeError):
                parsed_date = time_str

        entries.append({
            "source": "youtube",
            "title": title,
            "url": url,
            "channel": channel,
            "description": description,
            "date": parsed_date,
            "raw": item,
        })

    return entries


def extract_text_for_analysis(entries: list[dict]) -> list[str]:
    """Extract text chunks suitable for LLM analysis."""
    chunks = []
    for entry in entries:
        parts = [entry.get("title", "")]
        if entry.get("channel"):
            parts.append(f"by {entry['channel']}")
        if entry.get("description"):
            parts.append(entry["description"])
        text = " | ".join(p for p in parts if p)
        if text.strip():
            chunks.append(text)
    return chunks
