from __future__ import annotations

import math
import re


class ChatTokenEstimator:
    """
    Lightweight token estimator.

    This is NOT model-specific. It provides a fast approximation
    for statistics, context management, and future model routing.
    """

    WORDS_PER_TOKEN = 0.75

    # --------------------------------------------------

    def estimate(self, text: str) -> int:

        if not text:
            return 0

        text = re.sub(r"\s+", " ", text.strip())

        words = text.split()

        if not words:
            return 0

        return max(
            1,
            math.ceil(len(words) * self.WORDS_PER_TOKEN),
        )

    # --------------------------------------------------

    def estimate_messages(
        self,
        messages: list[dict],
    ) -> int:

        total = 0

        for message in messages:
            total += self.estimate(
                message.get("content", "")
            )

        return total

    # --------------------------------------------------

    def remaining(
        self,
        current_tokens: int,
        max_context: int,
    ) -> int:

        return max(
            0,
            max_context - current_tokens,
        )

    # --------------------------------------------------

    def percent_used(
        self,
        current_tokens: int,
        max_context: int,
    ) -> float:

        if max_context <= 0:
            return 0.0

        return round(
            (current_tokens / max_context) * 100,
            2,
        )


chat_token_estimator = ChatTokenEstimator()