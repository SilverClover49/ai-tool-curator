"""Main pipeline orchestrator."""

import sys
import json
import yaml
from pathlib import Path

from .ingest.youtube import parse_youtube_history, extract_text_for_analysis as yt_text
from .ingest.google_search import parse_google_activity, extract_text_for_analysis as g_text
from .extract.llm_client import LLMClient
from .extract.tool_extractor import extract_all_tools
from .extract.categorizer import categorize_all
from .vault.generator import generate_vault


def load_config(config_path: str = "config.yaml") -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def run(config_path: str = "config.yaml"):
    config = load_config(config_path)
    data_dir = config.get("data_dir", "data/raw")
    output_dir = config.get("vault", {}).get("output_dir", "vault")
    llm_config = config.get("llm", {})

    print("=" * 60)
    print("AI Tool Curator - Pipeline")
    print("=" * 60)

    # Step 1: Ingest
    print("\n[1/4] Ingesting history data...")
    all_texts = []

    yt_config = config.get("ingest", {}).get("youtube", {})
    if yt_config.get("enabled", True):
        print("  Scanning YouTube history...")
        yt_entries = parse_youtube_history(data_dir)
        print(f"  Found {len(yt_entries)} YouTube entries")
        all_texts.extend(yt_text(yt_entries))

    g_config = config.get("ingest", {}).get("google", {})
    if g_config.get("enabled", True):
        print("  Scanning Google activity...")
        g_entries = parse_google_activity(data_dir)
        print(f"  Found {len(g_entries)} Google entries")
        all_texts.extend(g_text(g_entries))

    print(f"  Total text chunks: {len(all_texts)}")

    if not all_texts:
        print("\n  No data found! Place your Google Takeout exports in data/raw/")
        print("  Supported files: *watch-history*.json, *MyActivity*.json")
        return

    # Step 2: Extract
    print("\n[2/4] Extracting AI tool mentions...")
    client = LLMClient(
        host=llm_config.get("host", "127.0.0.1"),
        port=llm_config.get("port", 8080),
    )

    if client.is_running():
        print("  LLM server detected - using keyword + LLM extraction")
        tools = extract_all_tools(client, all_texts)
    else:
        print("  LLM server not running - using keyword extraction only")
        from .extract.tool_extractor import keyword_extract
        raw = keyword_extract(all_texts)
        tools = [
            {
                "name": t["name"],
                "source": "keyword",
                "count": t["count"],
                "contexts": t["contexts"],
                "category": None,
                "url": None,
            }
            for t in raw
        ]

    print(f"  Extracted {len(tools)} unique tools")

    # Step 3: Categorize
    print("\n[3/4] Categorizing and rating tools...")
    if client.is_running():
        tools = categorize_all(client, tools)
    else:
        from .extract.categorizer import categorize_tool, rate_viability
        for tool in tools:
            ctx = " ".join(tool.get("contexts", []))
            tool["category"] = tool.get("category") or categorize_tool(tool["name"], ctx)
            tool["viability"] = rate_viability(tool["name"], tool.get("count", 1), ctx)

    # Step 4: Generate vault
    print("\n[4/4] Generating Obsidian vault...")
    generate_vault(tools, output_dir)

    # Save raw data
    processed_dir = Path("data/processed")
    processed_dir.mkdir(parents=True, exist_ok=True)
    with open(processed_dir / "tools.json", "w", encoding="utf-8") as f:
        json.dump(tools, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 60)
    print("Done! Open the 'vault' folder in Obsidian.")
    print("=" * 60)


if __name__ == "__main__":
    config = sys.argv[1] if len(sys.argv) > 1 else "config.yaml"
    run(config)
