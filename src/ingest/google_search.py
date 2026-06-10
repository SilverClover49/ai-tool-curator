"""Parse Google Search/Activity history from Google Takeout exports."""

import json
import os
from pathlib import Path
from datetime import datetime


def parse_google_activity(data_dir: str) -> list[dict]:
    """Parse Google My Activity JSON files from Google Takeout."""
    entries = []
    data_path = Path(data_dir)

    for json_file in data_path.rglob("*MyActivity*.json"):
        entries.extend(_parse_activity_file(json_file))

    for json_file in data_path.rglob("*search-history*.json"):
        entries.extend(_parse_activity_file(json_file))

    entries.sort(key=lambda x: x.get("date", ""), reverse=True)
    return entries


def _parse_activity_file(filepath: Path) -> list[dict]:
    """Parse a single Google Activity file."""
    entries = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return entries

    for item in data:
        header = item.get("header", "")
        title = item.get("title", "")
        time_str = item.get("time", "")
        url = ""
        subtitle = ""

        if "url" in item:
            url = item["url"]
        elif "header" in item and item["header"].startswith("http"):
            url = item["header"]

        if "subtitle" in item:
            subtitle = item["subtitle"]

        parsed_date = ""
        if time_str:
            try:
                dt = datetime.fromisoformat(time_str.replace("Z", "+00:00"))
                parsed_date = dt.strftime("%Y-%m-%d")
            except (ValueError, TypeError):
                parsed_date = time_str

        entries.append({
            "source": "google_search",
            "title": title,
            "url": url,
            "header": header,
            "subtitle": subtitle,
            "description": f"{header} {subtitle}".strip(),
            "date": parsed_date,
            "raw": item,
        })

    return entries


def extract_text_for_analysis(entries: list[dict]) -> list[str]:
    """Extract text chunks suitable for LLM analysis."""
    chunks = []
    for entry in entries:
        parts = [
            entry.get("title", ""),
            entry.get("header", ""),
            entry.get("subtitle", ""),
        ]
        text = " | ".join(p for p in parts if p)
        if text.strip():
            chunks.append(text)
    return chunks
