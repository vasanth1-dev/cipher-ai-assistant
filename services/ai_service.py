from core.logger import logger

from prompts.prompt_loader import prompt_loader

from services.history_service import history_service
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

        system_prompt, user_prompt = self._build_prompt(
            prompt
        )

        try:

            response = self.provider.generate(
                user_prompt,
                system=system_prompt,
            )

            if response is None:
                return ""

            response = str(response).strip()

            history_service.add(
                prompt,
                response,
            )

            return response

        except Exception as e:

            logger.exception(e)

            return (
                "Sorry, I couldn't generate a response."
            )

    # --------------------------------------------------
    # Streaming
    # --------------------------------------------------

    def stream(self, prompt):

        prompt = self._normalize(prompt)

        if not prompt:
            return

        system_prompt, user_prompt = self._build_prompt(
            prompt
        )

        try:

            logger.info(
                "[AI] Streaming response started."
            )

            chunks = []

            for chunk in self.provider.stream(
                user_prompt,
                system=system_prompt,
            ):

                if not chunk:
                    continue

                chunks.append(chunk)

                yield chunk

            if chunks:

                history_service.add(
                    prompt,
                    "".join(chunks),
                )

            logger.info(
                "[AI] Streaming response completed."
            )

        except Exception as e:

            logger.exception(e)

            yield (
                "Sorry, I couldn't generate a response."
            )

    # --------------------------------------------------
    # Prompt Builder
    # --------------------------------------------------

    def _build_prompt(
        self,
        prompt,
    ):

        prompt_lower = prompt.lower()

        system_parts = []

        # Always load

        for name in (

            "system_prompt",
            "router_prompt",

        ):

            text = prompt_loader.load(name)

            if text:
                system_parts.append(text)

        # Memory

        try:

            from services.memory_service import (
                memory_service,
            )

            memory = (
                memory_service.memory_prompt()
            )

            if memory:

                system_parts.append(memory)

        except Exception as e:

            logger.exception(e)

        # Coding

        coding_words = (

            "python",
            "java",
            "c++",
            "c#",
            "javascript",
            "html",
            "css",
            "sql",
            "code",
            "program",
            "debug",

        )

        if any(
            word in prompt_lower
            for word in coding_words
        ):

            system_parts.append(
                prompt_loader.load(
                    "coding_prompt"
                )
            )

            system_parts.append(
                prompt_loader.load(
                    "developer_prompt"
                )
            )

        # Linux

        linux_words = (

            "ubuntu",
            "linux",
            "terminal",
            "bash",
            "apt",
            "systemctl",
            "snap",

        )

        if any(
            word in prompt_lower
            for word in linux_words
        ):

            system_parts.append(
                prompt_loader.load(
                    "linux_prompt"
                )
            )

        # Interview

        if any(
            word in prompt_lower
            for word in (
                "interview",
                "mcq",
                "aptitude",
                "hr",
            )
        ):

            system_parts.append(
                prompt_loader.load(
                    "interview_prompt"
                )
            )

        # Concise

        if any(
            phrase in prompt_lower
            for phrase in (

                "full form",
                "meaning",
                "definition",

            )
        ):

            system_parts.append(
                prompt_loader.load(
                    "concise_prompt"
                )
            )

        # Detailed

        if any(
            word in prompt_lower
            for word in (

                "explain",
                "detail",
                "how",
                "why",
                "compare",

            )
        ):

            system_parts.append(
                prompt_loader.load(
                    "explanation_prompt"
                )
            )

        # Chat

        # Chat

            # --------------------------------------------------
        # Chat
        # --------------------------------------------------

        chat_words = (

            "hi",
            "hello",
            "hey",
            "good morning",
            "good afternoon",
            "good evening",
            "how are you",
            "who are you",

        )

        if any(
            word in prompt_lower
            for word in chat_words
        ):

            system_parts.append(
                prompt_loader.load(
                    "chat_prompt"
                )
            )

        # --------------------------------------------------
        # Memory Prompt (Only when needed)
        # --------------------------------------------------

        memory_words = (

            "remember",
            "forget",
            "my",
            "name",
            "favourite",
            "favorite",

        )

        if any(
            word in prompt_lower
            for word in memory_words
        ):

            system_parts.append(
                prompt_loader.load(
                    "memory_prompt"
                )
            )

        # --------------------------------------------------
        # User Memory
        # --------------------------------------------------

        try:

            from services.memory_service import (
                memory_service,
            )

            memory = (
                memory_service.memory_prompt()
            )

            if memory:

                system_parts.append(memory)

        except Exception as e:

            logger.exception(e)

        # --------------------------------------------------
        # Build System Prompt
        # --------------------------------------------------

        system_prompt = "\n\n".join(

            part

            for part in system_parts

            if part

        )

        return (
            system_prompt,
            prompt,
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