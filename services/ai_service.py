from core.logger import logger

from services.ollama_service import ollama_service


class AIService:

    def __init__(self):

        self.provider = ollama_service

    # --------------------------------------------------
    # Provider
    # --------------------------------------------------

    def set_provider(self, provider):

        if provider is None:
            return

        self.provider = provider

        logger.info(
            f"[AI] Provider changed to "
            f"{provider.__class__.__name__}"
        )

    def get_provider(self):

        return self.provider

    # --------------------------------------------------
    # Generate
    # --------------------------------------------------

    def generate(self, prompt):

        prompt = self._normalize(prompt)

        if not prompt:
            return ""

        if self.provider is None:
            return ""

        if not hasattr(self.provider, "generate"):
            logger.error(
                "[AI] Provider does not implement generate()."
            )
            return ""

        try:

            response = self.provider.generate(prompt)

            if response is None:
                return ""

            return str(response).strip()

        except Exception as e:

            logger.exception(e)

            return (
                "Sorry, I couldn't generate a response right now."
            )

    # --------------------------------------------------
    # Streaming
    # --------------------------------------------------

    def stream(self, prompt):

        prompt = self._normalize(prompt)

        if not prompt:
            return

        if self.provider is None:
            return

        if not hasattr(self.provider, "stream"):

            logger.error(
                "[AI] Provider does not implement stream()."
            )

            response = self.generate(prompt)

            if response:
                yield response

            return

        try:

            logger.info(
                "[AI] Streaming response started."
            )

            for chunk in self.provider.stream(prompt):

                if chunk is None:
                    continue

                chunk = str(chunk).strip()

                if not chunk:
                    continue

                yield chunk

            logger.info(
                "[AI] Streaming response completed."
            )

        except Exception as e:

            logger.exception(e)

            yield (
                "Sorry, I couldn't generate a response right now."
            )

    # --------------------------------------------------
    # Status
    # --------------------------------------------------

    def is_available(self):

        return self.provider is not None

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    @staticmethod
    def _normalize(prompt):

        if prompt is None:
            return ""

        return str(prompt).strip()


ai_service = AIService()