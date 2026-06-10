"""Categorize AI tools and assign viability ratings."""

from .llm_client import LLMClient


CATEGORY_KEYWORDS = {
    "Image Generation": [
        "stable diffusion", "midjourney", "dall-e", "comfyui", "flux", "sdxl",
        "automatic1111", "forge", "swarmui", "image gen", "text to image",
    ],
    "Video Generation": [
        "sora", "runway", "pika", "kling", "luma", "hailuo", "minimax video",
        "video gen", "text to video",
    ],
    "Coding Assistants": [
        "copilot", "cursor", "aider", "cline", "continue", "tabnine",
        "codeium", "windsurf", "supermaven", "bolt.new", "v0", "replit",
        "Devin", "open interpreter", "code gen", "coding",
    ],
    "AI Agents": [
        "autogpt", "babyagi", "crewai", "langchain", "llamaindex", "metagpt",
        "openai agents", "agentgpt", "agent", "orchestration",
    ],
    "Text/LLM": [
        "chatgpt", "openai", "claude", "anthropic", "gemini", "llama",
        "mistral", "deepseek", "gpt", "large language model", "llm",
    ],
    "Voice/Audio": [
        "elevenlabs", "whisper", "bark", "tortoise", "musicgen", "suno",
        "udio", "tts", "speech to text", "text to speech",
    ],
    "3D/Design": [
        "meshy", "tripo", "point-e", "shap-e", "3d gen", "3d model",
    ],
    "Search/RAG": [
        "perplexity", "you.com", "phind", "kagi", "searchgpt", "rag",
        "retrieval augmented",
    ],
    "Automation/No-Code": [
        "zapier ai", "make ai", "n8n", "flowise", "dify", "langflow",
        "automation", "no-code",
    ],
    "MLOps/Infrastructure": [
        "mlflow", "wandb", "weights", "mlops", "deploy", "serving",
        "inference", "gpu", "cuda", "tensorrt",
    ],
    "Data/Embeddings": [
        "pinecone", "weaviate", "chroma", "qdrant", "milvus", "embedding",
        "vector database", "vector store",
    ],
    "Vision/Multimodal": [
        "opencv", "vision", "image recognition", "object detection",
        "multimodal", "ocr",
    ],
    "Productivity": [
        "notion ai", "grammarly", "jasper", "copy.ai", "writesonic",
        "productivity", "writing",
    ],
    "Video Editing": [
        "descript", "capcut", "premiere", "editing", "video edit",
    ],
}


def categorize_tool(name: str, context: str = "") -> str:
    """Categorize a tool based on name and context keywords."""
    text = f"{name} {context}".lower()

    best_category = "Other"
    best_score = 0

    for category, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > best_score:
            best_score = score
            best_category = category

    return best_category


def rate_viability(name: str, mention_count: int, context: str = "") -> int:
    """Rate tool viability 1-5 based on mention frequency and context signals."""
    score = 3

    if mention_count >= 10:
        score += 1
    elif mention_count >= 5:
        score += 0.5

    text = f"{name} {context}".lower()
    positive = ["popular", "best", "amazing", "love", "great", "recommend",
                "essential", "must have", "daily", "favorite"]
    negative = ["bad", "terrible", "slow", "buggy", "hate", "avoid",
                "discontinued", "deprecated", "scam"]

    for word in positive:
        if word in text:
            score += 0.3
    for word in negative:
        if word in text:
            score -= 0.3

    return max(1, min(5, round(score)))


def categorize_all(client: LLMClient, tools: list[dict]) -> list[dict]:
    """Categorize and rate all extracted tools."""
    for tool in tools:
        name = tool.get("name", "")
        contexts = tool.get("contexts", [])
        context_text = " ".join(contexts)

        tool["category"] = tool.get("category") or categorize_tool(name, context_text)
        tool["viability"] = rate_viability(name, tool.get("count", 1), context_text)

    llm_batch = [t for t in tools if t.get("category") == "Other" and t.get("count", 1) >= 3]
    if llm_batch and client.is_running():
        names = [t["name"] for t in llm_batch]
        prompt = f"""For each AI tool below, provide:
1. category (one of: Image Generation, Video Generation, Coding Assistants, AI Agents, Text/LLM, Voice/Audio, 3D/Design, Search/RAG, Automation/No-Code, MLOps/Infrastructure, Data/Embeddings, Vision/Multimodal, Productivity, Video Editing, Other)
2. viability (1-5, where 5=industry standard, 4=widely used, 3=solid option, 2=niche, 1=experimental/abandoned)

Tools: {json.dumps(names)}

Return JSON array: [{{"name": "...", "category": "...", "viability": N}}]"""

        response = client.chat(
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=1024,
        )
        result = client.extract_json(response)
        if isinstance(result, list):
            lookup = {r["name"].lower(): r for r in result if "name" in r}
            for tool in llm_batch:
                llm_data = lookup.get(tool["name"].lower())
                if llm_data:
                    tool["category"] = llm_data.get("category", tool["category"])
                    tool["viability"] = llm_data.get("viability", tool["viability"])

    return tools
