import requests

from config import (
    OLLAMA_URL,
    OLLAMA_MODEL,
    AI_PERSONALITY,
)


class OllamaService:

    def __init__(self):
        self.url = OLLAMA_URL
        self.model = OLLAMA_MODEL

    def ask(self, prompt: str):

        if not prompt:
            return "I didn't hear anything."

        try:

            response = requests.post(
                self.url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "system": AI_PERSONALITY,
                    "stream": False,
                },
                timeout=120,
            )

            response.raise_for_status()

            data = response.json()

            return data.get(
                "response",
                "Sorry, I couldn't generate a response."
            ).strip()

        except requests.exceptions.ConnectionError:
            return "Ollama is not running."

        except requests.exceptions.Timeout:
            return "Ollama took too long to respond."

        except Exception as e:
            return f"Ollama Error: {e}"


ollama_service = OllamaService()