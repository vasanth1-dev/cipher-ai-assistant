from __future__ import annotations

import re
from collections import Counter


class ChatSummaryService:
    """
    Generates lightweight conversation summaries.

    This service does not use an LLM.
    It provides a fast local summary that can later be
    replaced with AI-generated summaries.
    """

    STOP_WORDS = {
        "the", "a", "an", "and", "or", "to", "of",
        "is", "are", "was", "were", "in", "on",
        "for", "with", "that", "this", "it",
        "you", "your", "i", "we", "they",
        "be", "as", "at", "by", "from",
    }

    # --------------------------------------------------

    def summarize(
        self,
        messages: list[dict],
        max_sentences: int = 5,
    ) -> dict:

        if not messages:
            return {
                "summary": "",
                "keywords": [],
                "message_count": 0,
            }

        text = "\n".join(
            str(message.get("content", ""))
            for message in messages
        )

        sentences = [
            sentence.strip()
            for sentence in re.split(
                r"[.!?]\s+",
                text,
            )
            if sentence.strip()
        ]

        summary = " ".join(
            sentences[:max_sentences]
        )

        keywords = self.extract_keywords(text)

        return {
            "summary": summary,
            "keywords": keywords,
            "message_count": len(messages),
        }

    # --------------------------------------------------

    def extract_keywords(
        self,
        text: str,
        limit: int = 10,
    ) -> list[str]:

        words = re.findall(
            r"[A-Za-z0-9_]+",
            text.lower(),
        )

        words = [
            word
            for word in words
            if word not in self.STOP_WORDS
            and len(word) > 2
        ]

        counter = Counter(words)

        return [
            word
            for word, _ in counter.most_common(limit)
        ]


chat_summary_service = ChatSummaryService()