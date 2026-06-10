"""Client for communicating with llama-server via HTTP API."""

import json
import time
import requests


class LLMClient:
    def __init__(self, host: str = "127.0.0.1", port: int = 8080):
        self.base_url = f"http://{host}:{port}"
        self.session = requests.Session()

    def is_running(self) -> bool:
        try:
            r = self.session.get(f"{self.base_url}/health", timeout=5)
            return r.status_code == 200
        except requests.ConnectionError:
            return False

    def wait_for_server(self, timeout: int = 120) -> bool:
        start = time.time()
        while time.time() - start < timeout:
            if self.is_running():
                return True
            time.sleep(2)
        return False

    def chat(self, messages: list[dict], temperature: float = 0.3,
             max_tokens: int = 2048) -> str:
        """Send a chat completion request."""
        payload = {
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False,
        }
        r = self.session.post(
            f"{self.base_url}/v1/chat/completions",
            json=payload,
            timeout=120,
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]

    def complete(self, prompt: str, temperature: float = 0.3,
                 max_tokens: int = 2048) -> str:
        """Send a completion request."""
        payload = {
            "prompt": prompt,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False,
        }
        r = self.session.post(
            f"{self.base_url}/v1/completions",
            json=payload,
            timeout=120,
        )
        r.raise_for_status()
        return r.json()["choices"][0]["text"]

    def extract_json(self, text: str) -> dict | list | None:
        """Try to extract JSON from LLM response text."""
        text = text.strip()
        if text.startswith("```"):
            lines = text.split("\n")
            lines = [l for l in lines if not l.strip().startswith("```")]
            text = "\n".join(lines)

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        start = text.find("[")
        if start != -1:
            end = text.rfind("]")
            if end > start:
                try:
                    return json.loads(text[start:end + 1])
                except json.JSONDecodeError:
                    pass

        start = text.find("{")
        if start != -1:
            end = text.rfind("}")
            if end > start:
                try:
                    return json.loads(text[start:end + 1])
                except json.JSONDecodeError:
                    pass

        return None
