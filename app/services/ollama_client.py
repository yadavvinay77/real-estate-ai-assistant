# app/services/ollama_client.py

import requests
from app.config import get_settings

settings = get_settings()

class OllamaClient:

    def __init__(self, model_name: str | None = None):
        self.model = model_name or settings.OLLAMA_MODEL
        self.url = "http://localhost:11434/api/generate"

    def generate(self, prompt: str, max_tokens: int = 512) -> str:
        """
        Sends prompt to Ollama server and returns AI response.
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }

        try:
            response = requests.post(self.url, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "").strip()

        except Exception as e:
            print("❌ Ollama error:", e)
            return "There was an issue communicating with the local AI engine."
