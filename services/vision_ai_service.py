import base64
import requests

from config import OLLAMA_URL


class VisionAIService:

    def __init__(self):
        self.url = OLLAMA_URL
        self.model = "qwen2.5vl:3b"

    def describe(self, image_path: str, prompt: str = "Describe this image."):

        try:
            with open(image_path, "rb") as f:
                image_data = base64.b64encode(f.read()).decode("utf-8")

            response = requests.post(
                self.url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "images": [image_data],
                    "stream": False,
                },
                timeout=300,
            )

            response.raise_for_status()

            data = response.json()

            return data.get("response", "No response.")

        except Exception as e:
            return f"Vision Error: {e}"


vision_ai_service = VisionAIService()