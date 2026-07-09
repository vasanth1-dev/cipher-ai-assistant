from __future__ import annotations

import re


class ChatTitleService:
    """
    Generates short conversation titles.

    Examples:
        "Explain Python decorators" -> "Explain Python decorators"
        "How do I install Ollama on Ubuntu?" -> "Install Ollama on Ubuntu"
    """

    MAX_LENGTH = 40

    _STOP_WORDS = {
        "please",
        "can",
        "could",
        "would",
        "you",
        "me",
        "the",
        "a",
        "an",
    }

    # --------------------------------------------------

    def generate(self, text: str) -> str:

        text = text.strip()

        if not text:
            return "New Chat"

        text = re.sub(r"\s+", " ", text)

        words = text.split()

        cleaned = [
            word
            for word in words
            if word.lower() not in self._STOP_WORDS
        ]

        if cleaned:
            title = " ".join(cleaned)
        else:
            title = text

        if len(title) > self.MAX_LENGTH:
            title = title[: self.MAX_LENGTH].rstrip() + "..."

        return title

    # --------------------------------------------------

    def from_messages(
        self,
        messages: list[dict],
    ) -> str:

        for message in messages:

            if message.get("role") == "user":
                return self.generate(
                    message.get("content", "")
                )

        return "New Chat"


chat_title_service = ChatTitleService()