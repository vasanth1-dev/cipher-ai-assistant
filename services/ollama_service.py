import json

import requests

from config import (
    MODEL_NAME,
    OLLAMA_URL,
)

from core.logger import logger


class OllamaService:

    def __init__(
       self,
    ) -> None:

        self.url = OLLAMA_URL
        self.model = MODEL_NAME

        self.timeout = 300

        self.session = requests.Session()

        self.options = {
            "temperature": 0.2,
            "top_p": 0.9,
            "num_predict": 512,
        }

    # --------------------------------------------------
    # Generate
    # --------------------------------------------------

    def generate(
        self,
        prompt: str,
        system: str = "",
    ) -> str:

        prompt = self._normalize(prompt)

        if not prompt:
            return ""

        try:

            payload = self._build_payload(
                prompt,
                system,
                False,
            )

            response = self._post(
                payload,
            )

            response.raise_for_status()

            logger.debug(
                "[OLLAMA] Response recieved."
            )

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

            logger.exception(
                f"[OLLAMA] Generate failed: {e}"
            )

            

            return (
                "I'm unable to connect to the AI model."
            )

    # --------------------------------------------------
    # Stream
    # --------------------------------------------------
    from collections.abc import Iterator


    def stream(
        self,
        prompt: str,
        system: str = "",
    ) -> Iterator[str]:

        prompt = self._normalize(prompt)

        if not prompt:
            return

        try:

            payload = self._build_payload(
                prompt,
                system,
                True,
            )

            with self._post(
                payload,
                stream = True,
            ) as response:

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

                            logger.info(
                                "[OLLAMA] Streaming completed."
                            )

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

            logger.exception(
                f"[OLLAMA] Stream failed: {e}"
            )

            yield (
                "I'm unable to connect to the AI model."
            )

    # --------------------------------------------------
    # Status
    # --------------------------------------------------

    def is_available(
        self
    ) -> bool:

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
    ) -> None:

        if model_name:

            self.model = model_name

    def get_model(
        self,
    ) -> str:

        return self.model
    
    def _build_payload(
        self,
        prompt: str,
        system: str,
        stream: bool,
    ) -> dict:
        """
        Build the Ollama request payload.
        """

        return {
            "model": self.model,
            "system": system,
            "prompt": prompt,
            "stream": stream,
            "options": self.options,
        }
    

    def _post(
        self,
        payload: dict,
        stream: bool = False,
    ):
        """
        Send a request to Ollama.
        """

        return self.session.post(
            self.url,
            json=payload,
            stream=stream,
            timeout=self.timeout,
        )

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    @staticmethod
    def _normalize(
        prompt: str | None,
    ) -> str:

        if prompt is None:
            return ""

        return str(prompt).strip()


ollama_service = OllamaService()