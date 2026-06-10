"""Generate Obsidian vault from extracted AI tool data."""

import os
import re
from pathlib import Path
from datetime import datetime


def sanitize_filename(name: str) -> str:
    """Make a string safe for use as a filename."""
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name[:100]


def generate_tool_note(tool: dict, output_dir: Path) -> str:
    """Generate a markdown note for a single AI tool."""
    name = tool["name"]
    category = tool.get("category", "Other")
    viability = tool.get("viability", 3)
    count = tool.get("count", 1)
    url = tool.get("url", "")
    contexts = tool.get("contexts", [])

    stars = "★" * viability + "☆" * (5 - viability)

    lines = [
        f"---",
        f"category: {category}",
        f"viability: {viability}/5",
        f"mentions: {count}",
        f"date_added: {datetime.now().strftime('%Y-%m-%d')}",
        f"tags: [ai-tool, {category.lower().replace(' ', '-')}]",
        f"---",
        f"",
        f"# {name}",
        f"",
        f"**Category:** [[_index/{category}|{category}]]",
        f"**Viability:** {stars} ({viability}/5)",
        f"**Mentioned {count} time{'s' if count != 1 else ''} in your history**",
        f"",
    ]

    if url:
        lines.append(f"**URL:** [{url}]({url})")
        lines.append("")

    if contexts:
        lines.append("## Context")
        lines.append("")
        for ctx in contexts[:5]:
            lines.append(f"> {ctx}")
            lines.append("")

    lines.append("## Notes")
    lines.append("")
    lines.append("_Add your notes about this tool here._")
    lines.append("")

    filename = sanitize_filename(name) + ".md"
    filepath = output_dir / filename
    filepath.write_text("\n".join(lines), encoding="utf-8")
    return filename


def generate_category_index(category: str, tools: list[dict], output_dir: Path):
    """Generate a category index note."""
    lines = [
        f"---",
        f"tags: [ai-tool-index, {category.lower().replace(' ', '-')}]",  
        f"---",
        f"",
        f"# {category}",
        f"",
        f"## Tools ({len(tools)})",
        f"",
        f"| Tool | Viability | Mentions |",
        f"|------|-----------|----------|",
    ]

    for tool in sorted(tools, key=lambda x: x.get("viability", 0), reverse=True):
        name = tool["name"]
        v = tool.get("viability", 3)
        c = tool.get("count", 1)
        stars = "★" * v
        lines.append(f"| [[{name}]] | {stars} | {c} |")

    lines.append("")
    lines.append(f"[[{_moc_name()}|Back to MOC]]")
    lines.append("")

    filepath = output_dir / f"{category}.md"
    filepath.write_text("\n".join(lines), encoding="utf-8")


def _moc_name() -> str:
    return "_MOC"


def generate_moc(tools: list[dict], output_dir: Path):
    """Generate the master Map of Content."""
    categories = {}
    for tool in tools:
        cat = tool.get("category", "Other")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(tool)

    lines = [
        f"---",
        f"tags: [moc]",
        f"---",
        f"",
        f"# AI Tool Map",
        f"",
        f"_Auto-generated from your YouTube, Google, and search history._",
        f"_Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}_",
        f"",
        f"## Stats",
        f"",
        f"- **Total tools found:** {len(tools)}",
        f"- **Categories:** {len(categories)}",
        f"- **Top tools by mentions:**",
    ]

    for tool in tools[:10]:
        lines.append(f"  1. [[{tool['name']}]] ({tool.get('count', 1)} mentions)")

    lines.append("")
    lines.append("## Categories")
    lines.append("")

    for cat in sorted(categories.keys()):
        cat_tools = categories[cat]
        lines.append(f"### [[_index/{cat}|{cat}]] ({len(cat_tools)} tools)")
        for tool in sorted(cat_tools, key=lambda x: x.get("viability", 0), reverse=True)[:5]:
            v = tool.get("viability", 3)
            stars = "★" * v
            lines.append(f"- [[{tool['name']}]] {stars}")
        lines.append("")

    lines.append("## All Tools (by viability)")
    lines.append("")
    lines.append("| Tool | Category | Viability | Mentions |")
    lines.append("|------|----------|-----------|----------|")

    for tool in sorted(tools, key=lambda x: (x.get("viability", 0), x.get("count", 0)), reverse=True):
        name = tool["name"]
        cat = tool.get("category", "Other")
        v = tool.get("viability", 3)
        c = tool.get("count", 1)
        lines.append(f"| [[{name}]] | {cat} | {'★' * v} | {c} |")

    lines.append("")

    filepath = output_dir / "_MOC.md"
    filepath.write_text("\n".join(lines), encoding="utf-8")


def generate_vault(tools: list[dict], output_dir: str):
    """Generate the complete Obsidian vault."""
    out = Path(output_dir)
    tools_dir = out / "tools"
    index_dir = out / "_index"

    tools_dir.mkdir(parents=True, exist_ok=True)
    index_dir.mkdir(parents=True, exist_ok=True)

    print(f"  Generating {len(tools)} tool notes...")
    for tool in tools:
        generate_tool_note(tool, tools_dir)

    categories = {}
    for tool in tools:
        cat = tool.get("category", "Other")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(tool)

    print(f"  Generating {len(categories)} category indexes...")
    for cat, cat_tools in categories.items():
        generate_category_index(cat, cat_tools, index_dir)

    print(f"  Generating MOC...")
    generate_moc(tools, out)

    print(f"  Vault generated at: {out}")
