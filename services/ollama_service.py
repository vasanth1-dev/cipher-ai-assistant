import json

import requests

from config import (
    MODEL_NAME,
    OLLAMA_URL,
)

from core.logger import logger


class OllamaService:

    def __init__(self):

        self.url = OLLAMA_URL
        self.model = MODEL_NAME

        self.timeout = 300

        self.session = requests.Session()

    # --------------------------------------------------
    # Generate
    # --------------------------------------------------

    def generate(
        self,
        prompt: str,
        system: str = "",
    ):

        prompt = self._normalize(prompt)

        if not prompt:
            return ""

        try:

            payload = {

                "model": self.model,

                "system": system,

                "prompt": prompt,

                "stream": False,

                "options": {

                    "temperature": 0.2,
                    "top_p": 0.9,
                    "num_predict": 512,

                },

            }

            response = self.session.post(

                self.url,

                json=payload,

                timeout=self.timeout,

            )

            response.raise_for_status()

            data = response.json()

            return str(
                data.get(
                    "response",
                    "",
                )
            ).strip()

        except requests.exceptions.Timeout:

            logger.exception(
                "Ollama request timed out."
            )

            return (
                "The AI model took too long to respond."
            )

        except Exception as e:

            logger.exception(e)

            print(
                f"\nOLLAMA STREAM ERROR: {type(e).__name__}: {e}\n"
            )

            return (
                "I'm unable to connect to the AI model."
            )

    # --------------------------------------------------
    # Stream
    # --------------------------------------------------

    def stream(
        self,
        prompt: str,
        system: str = "",
    ):

        prompt = self._normalize(prompt)

        if not prompt:
            return

        try:

            payload = {

                "model": self.model,

                "system": system,

                "prompt": prompt,

                "stream": True,

                "options": {

                    "temperature": 0.2,
                    "top_p": 0.9,
                    "num_predict": 512,

                },

            }

            response = self.session.post(

                self.url,

                json=payload,

                stream=True,

                timeout=self.timeout,

            )

            response.raise_for_status()

            for line in response.iter_lines(decode_unicode=True):

                if not line:
                    continue

                try:

                    data = json.loads(line)

                    text = data.get(
                        "response",
                        "",
                    )

                    if text:
                        yield text

                    if data.get("done"):
                        break

                except Exception:

                    continue

        except requests.exceptions.Timeout:

            logger.exception(
                "Ollama stream timed out."
            )

            yield (
                "The AI model took too long to respond."
            )

        except Exception as e:

            logger.exception(e)

            print(
                f"\nOLLAMA STREAM ERROR: {type(e).__name__}: {e}\n"
            )

            yield (
                "I'm unable to connect to the AI model."
            )

    # --------------------------------------------------
    # Status
    # --------------------------------------------------

    def is_available(self):

        try:

            response = self.session.get(

                self.url.replace(
                    "/generate",
                    "/tags",
                ),

                timeout=5,

            )

            response.raise_for_status()
            return True

        except Exception:

            return False

    # --------------------------------------------------
    # Model
    # --------------------------------------------------

    def set_model(
        self,
        model_name: str,
    ):

        if model_name:

            self.model = model_name

    def get_model(self):

        return self.model

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    @staticmethod
    def _normalize(prompt):

        if prompt is None:
            return ""

        return str(prompt).strip()


ollama_service = OllamaService()