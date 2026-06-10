"""Extract AI tool mentions from text using LLM + keyword matching."""

import json
import re
from pathlib import Path

from .llm_client import LLMClient


KNOWN_AI_TOOLS = {
    "chatgpt", "openai", "gpt-4", "gpt-4o", "gpt-3.5", "gpt-5",
    "claude", "anthropic", "claude 3", "claude 4", "sonnet", "opus", "haiku",
    "gemini", "google gemini", "bard",
    "midjourney", "dall-e", "dalle", "stable diffusion", "comfyui", "flux",
    "sdxl", "sd xl", "automatic1111", "a1111", "forge", "swarmui",
    "sora", "runway", "pika", "kling", "luma", "hailuo", "minimax video",
    "copilot", "github copilot", "cursor", "aider", "cline", "continue",
    "tabnine", "codeium", "windsurf", "supermaven", "bolt.new", "v0",
    "replit", "Devin", "open interpreter",
    "autogpt", "babyagi", "crewai", "langchain", "llamaindex", "metagpt",
    "openai agents", "agentgpt", "huggingface agents",
    "elevenlabs", "whisper", "bark", "tortoise", "musicgen", "suno", "udio",
    "meshy", "tripo", "point-e", "shap-e", "luma dream machine",
    "perplexity", "you.com", "phind", "kagi", "searchgpt",
    "zapier ai", "make ai", "n8n", "flowise", "dify", "langflow",
    "ollama", "llama", "llama.cpp", "llamacpp", "lm studio", "lmstudio",
    "jan", "gpt4all", "localai", "text-generation-webui",
    "hugging face", "huggingface", "hugging face transformers",
    "pytorch", "tensorflow", "keras", "jax",
    "opencv", "pillow", "ffmpeg",
    "notion ai", "grammarly", "jasper", "copy.ai", "writesonic",
    "synthesia", "heygen", "d-id", "colossyan",
    "runway ml", "kaiber", "deepbrain",
    "nvidia", "cuda", "tensorrt", "onnx", "onnxruntime",
    "pinecone", "weaviate", "chroma", "chromadb", "qdrant", "milvus",
    "openai api", "anthropic api", "cohere", "ai21", "mistral",
    "deepseek", "moonshot", "kimi", "zhipu", "glm",
    "minimax", "baichuan", "01.ai", "yi",
    "mlops", "mlflow", "weights & biases", "wandb",
    "labelstudio", "label studio", "roboflow",
    "gradio", "streamlit", "panel",
    "kaggle", "colab", "google colab",
    "figma ai", "canva ai", "adobe firefly", "photoshop ai",
    "descript", "capcut", "premiere ai",
    "ai tool", "ai model", "machine learning", "deep learning",
    "neural network", "transformer", "diffusion model",
}

TOOL_PATTERN = re.compile(
    r'\b(' + '|'.join(re.escape(t) for t in sorted(KNOWN_AI_TOOLS, key=len, reverse=True)) + r')\b',
    re.IGNORECASE
)


def keyword_extract(texts: list[str]) -> list[dict]:
    """First pass: extract known AI tools via keyword matching."""
    found = {}
    for text in texts:
        matches = TOOL_PATTERN.findall(text)
        for match in matches:
            normalized = match.lower().strip()
            if normalized not in found:
                found[normalized] = {
                    "name": match,
                    "count": 0,
                    "contexts": [],
                }
            found[normalized]["count"] += 1
            if len(found[normalized]["contexts"]) < 3:
                found[normalized]["contexts"].append(text[:200])

    return sorted(found.values(), key=lambda x: x["count"], reverse=True)


def llm_extract(client: LLMClient, texts: list[str],
                batch_size: int = 20) -> list[dict]:
    """Second pass: use LLM to find unknown AI tool mentions."""
    all_tools = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        numbered = "\n".join(f"{j+1}. {t}" for j, t in enumerate(batch))

        prompt = f"""Analyze these entries and identify ANY AI tools, AI models, AI services, or ML frameworks mentioned.

Entries:
{numbered}

Return ONLY a JSON array. Each item: {{"name": "tool name", "category": "category", "url_if_known": "url or null"}}
If no AI tools found, return empty array [].

JSON:"""

        response = client.chat(
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=1024,
        )

        result = client.extract_json(response)
        if isinstance(result, list):
            all_tools.extend(result)

    return all_tools


def extract_all_tools(client: LLMClient, texts: list[str]) -> list[dict]:
    """Run full extraction pipeline: keywords first, then LLM for unknowns."""
    known = keyword_extract(texts)
    print(f"  Keyword pass found {len(known)} known tools")

    llm_tools = llm_extract(client, texts)
    print(f"  LLM pass found {len(llm_tools)} additional tools")

    merged = {}
    for tool in known:
        name = tool["name"].lower()
        merged[name] = {
            "name": tool["name"],
            "source": "keyword",
            "count": tool["count"],
            "contexts": tool["contexts"],
            "category": None,
            "url": None,
        }

    for tool in llm_tools:
        name = tool.get("name", "").lower()
        if name and name not in merged:
            merged[name] = {
                "name": tool["name"],
                "source": "llm",
                "count": 1,
                "contexts": [],
                "category": tool.get("category"),
                "url": tool.get("url_if_known"),
            }

    return sorted(merged.values(), key=lambda x: x.get("count", 0), reverse=True)
