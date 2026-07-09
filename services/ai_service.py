from core.logger import logger

from services.ollama_service import ollama_service
from services.history_service import history_service

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
        prompt = self._build_prompt(prompt)

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
            
            response = str(response).strip()
        
            try:
                history_service.add(
                    prompt,
                    response,
                )

            except Exception as e:
                logger.exception(e)

            return response

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
        prompt = self._build_prompt(prompt)

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

                # IMPORTANT:
                # Don't strip streaming chunks.
                # Ollama sends leading/trailing spaces in many chunks.
                chunk = str(chunk)

                if chunk == "":
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
    
    def _build_prompt(
        self,
        prompt,
    ):
        """
        Build the final AI prompt.

        Currently returns the prompt unchanged.

        Later this method will include:
        - conversation history
        - memory
        - system prompt
        - user profile
        """

        try:
            from services.memory_service import memory_service

            memory = memory_service.export()

            if memory:

                return(
                    "Known information about the user:\n"
                    f"{memory}\n\n"
                    f"User: {prompt}\n"
                    "Cipher"
                )
            

        except Exception as e:

            logger.exception(e)

        return prompt

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    @staticmethod
    def _normalize(prompt):

        if prompt is None:
            return ""

        return str(prompt).strip()


ai_service = AIService()