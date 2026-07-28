from core.logger import logger

from prompts.prompt_loader import prompt_loader

from services.history_service import history_service
from services.question_classifier import question_classifier
from services.memory_service import memory_service
from services.ollama_service import ollama_service


class AIService:

        # --------------------------------------------------
    # Prompt Keywords
    # --------------------------------------------------

    CODING_WORDS = (
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

    LINUX_WORDS = (
        "ubuntu",
        "linux",
        "terminal",
        "bash",
        "apt",
        "systemctl",
        "snap",
    )

    INTERVIEW_WORDS = (
        "interview",
        "mcq",
        "aptitude",
        "hr",
    )

    CONCISE_WORDS = (
        "full form",
        "meaning",
        "definition",
    )

    EXPLANATION_WORDS = (
        "explain",
        "detail",
        "how",
        "why",
        "compare",
    )

    CHAT_WORDS = (
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening",
        "how are you",
        "who are you",
    )

    MEMORY_WORDS = (
        "remember",
        "forget",
        "my",
        "name",
        "favourite",
        "favorite",
    )

    def __init__(
       self,
    ) -> None:

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

    def generate(self, prompt):

        prompt = self._normalize(prompt)

        if not prompt:
            return ""

        if question_classifier.is_simple(prompt):

            system_instruction = """
    You are Cipher.

    The user asked a simple factual question.

    Answer in ONLY 2 to 4 sentences.

    Do not use headings.

    Do not use bullet points.

    Do not give unnecessary details.

    Keep the answer under 80 words.
    """

        else:

            system_instruction = """
    You are Cipher.

    Match the response length to the user's request.

    If the user asks for details,
    provide a complete and well-structured explanation.

    Use headings and bullet points whenever helpful.
    """

        try:

            logger.debug("STEP 1: Before _build_prompt")

            system_prompt, user_prompt = self._build_prompt(prompt)

            logger.debug(
                f"STEP 2: Prompt built (system={len(system_prompt)}, user={len(user_prompt)})"
            )

            # Merge classifier instruction
            system_prompt = f"""
    {system_prompt}

    {system_instruction}
    """

            logger.debug("STEP 3: Before provider.generate()")

            response = self.provider.generate(
                user_prompt,
                system=system_prompt,
            )

            logger.debug("STEP 4: After provider.generate()")

            if response is None:
                return ""

            response = str(response).strip()

            logger.debug(
                f"STEP 5: Response received ({len(response)} characters)"
            )

            history_service.add(
                prompt,
                response,
            )

            logger.debug("STEP 6: History saved")

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


    def _add_prompt(
        self,
        system_parts: list[str],
        prompt_name: str,
    ) -> None:
        """
        Load a system prompt and add it if available.
        """

        prompt = prompt_loader.load(prompt_name)

        if prompt:
            system_parts.append(prompt)

    # --------------------------------------------------
    # Prompt Builder
    # --------------------------------------------------
    
    def _load_memory(
        self,
        system_parts: list[str],
    ) -> None:
        """
        Load memory prompt into the system prompt list.
        """

        try:

            memory = memory_service.memory_prompt()

            if memory:
                system_parts.append(memory)

        except Exception as e:

            logger.exception(e)

    def _contains_any(
        self,
        text: str,
        keywords: tuple[str, ...],
    ) -> bool:
        """
        Return True if any keyword exists in the text.
        """

        return any(
            keyword in text
            for keyword in keywords
        )
    
    def _load_base_prompts(
        self,
        system_parts: list[str],
    ) -> None:
        """
        Load the default system prompts.
        """

        self._add_prompt(
            system_parts,
            "system_prompt",
        )

        self._add_prompt(
            system_parts,
            "router_prompt",
        )

    def _load_category_prompts(
        self,
        prompt_lower: str,
        system_parts: list[str],
    ) -> None:
        """
        Load additional prompts based on the user's request.
        """

        # --------------------------------------------------
        # Coding
        # --------------------------------------------------

        if self._contains_any(
            prompt_lower,
            self.CODING_WORDS,
        ):

            self._add_prompt(
                system_parts,
                "coding_prompt",
            )

            self._add_prompt(
                system_parts,
                "developer_prompt",
            )

        # --------------------------------------------------
        # Linux
        # --------------------------------------------------

        if self._contains_any(
            prompt_lower,
            self.LINUX_WORDS,
        ):

            self._add_prompt(
                system_parts,
                "linux_prompt",
            )

        # --------------------------------------------------
        # Interview
        # --------------------------------------------------

        if self._contains_any(
            prompt_lower,
            self.INTERVIEW_WORDS,
        ):

            self._add_prompt(
                system_parts,
                "interview_prompt",
            )

        # --------------------------------------------------
        # Concise
        # --------------------------------------------------

        if self._contains_any(
            prompt_lower,
            self.CONCISE_WORDS,
        ):

            self._add_prompt(
                system_parts,
                "concise_prompt",
            )

        # --------------------------------------------------
        # Detailed Explanation
        # --------------------------------------------------

        if self._contains_any(
            prompt_lower,
            self.EXPLANATION_WORDS,
        ):

            self._add_prompt(
                system_parts,
                "explanation_prompt",
            )

        # --------------------------------------------------
        # Chat
        # --------------------------------------------------

        if self._contains_any(
            prompt_lower,
            self.CHAT_WORDS,
        ):

            self._add_prompt(
                system_parts,
                "chat_prompt",
            )

        # --------------------------------------------------
        # Memory Prompt
        # --------------------------------------------------

        if self._contains_any(
            prompt_lower,
            self.MEMORY_WORDS,
        ):

            self._add_prompt(
                system_parts,
                "memory_prompt",
            )

    def _build_system_prompt(
        self,
        system_parts: list[str],
    ) -> str:
        """
        Combine all prompt parts into a single system prompt.
        """

        return "\n\n".join(

            part.strip()

            for part in system_parts

            if part

        )

    def _build_prompt(
        self,
        prompt: str,
    ) -> tuple[str, str]:
        """
        Build the complete system prompt for the AI model.
        """

        prompt_lower = prompt.lower()

        system_parts: list[str] = []

        # --------------------------------------------------
        # Base Prompts
        # --------------------------------------------------

        self._add_prompt(
            system_parts,
            "system_prompt",
        )

        self._add_prompt(
            system_parts,
            "router_prompt",
        )

        # --------------------------------------------------
        # User Memory
        # --------------------------------------------------

        self._load_memory(system_parts)

        # --------------------------------------------------
        # Category Prompts
        # --------------------------------------------------

        self._load_category_prompts(
            prompt_lower,
            system_parts,
        )

        # --------------------------------------------------
        # Build Final System Prompt
        # --------------------------------------------------

        system_prompt = self._build_system_prompt(
            system_parts,
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