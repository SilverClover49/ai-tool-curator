# AI Tool Curator

Scans your YouTube, Google Search, and WhatsApp history to discover every AI tool you've ever encountered, then generates a structured Obsidian vault organized by category with viability ratings.

## How It Works

1. **Ingest** — Parse YouTube watch history, Google My Activity exports, and WhatsApp chat exports
2. **Extract** — Use a local LLM (Gemma 4 E4B via llama.cpp) to identify AI tool mentions, extract names, URLs, and context
3. **Categorize** — Classify each tool by domain (image gen, coding, agents, etc.) and rate viability
4. **Generate** — Output an Obsidian vault with MOC indexes, per-tool notes, and backlinks to source material

## Setup

```cmd
setup.cmd
```

This will:
- Install CMake via MSYS2
- Build llama.cpp with CUDA support
- Download the Gemma 4 E4B GGUF model
- Install Python dependencies

## Usage

1. Export your data:
   - YouTube/Google: [takeout.google.com](https://takeout.google.com) → select YouTube History + My Activity
   - WhatsApp: Chat export → .txt files
2. Place exports in `data/raw/`
3. Run the pipeline:

```cmd
run.cmd
```

4. Open the `vault/` folder in Obsidian

## Configuration

Edit `config.yaml` to adjust:
- LLM settings (model, context length, GPU layers)
- Category definitions
- Viability rating criteria
- Obsidian vault structure

## Project Structure

```
ai-tool-curator/
├── llama.cpp/          # Self-contained llama.cpp build
├── data/               # Input data and processing cache
├── src/                # Python pipeline
│   ├── ingest/         # Data parsers (YouTube, Google, WhatsApp)
│   ├── extract/        # LLM-based tool extraction
│   └── vault/          # Obsidian vault generator
├── vault/              # Generated Obsidian vault output
├── config.yaml         # Settings
└── run.cmd             # One-click run
```

## License

MIT
