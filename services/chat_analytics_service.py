from __future__ import annotations

from collections import Counter


class ChatAnalyticsService:
    """
    Provides lightweight analytics for a conversation.

    Expected message format:
    {
        "role": "user" | "assistant" | "system",
        "content": "..."
    }
    """

    # --------------------------------------------------

    def analyze(
        self,
        messages: list[dict],
    ) -> dict:

        role_counter = Counter()

        characters = 0
        words = 0
        longest_message = 0

        for message in messages:

            role = message.get(
                "role",
                "assistant",
            )

            content = str(
                message.get(
                    "content",
                    "",
                )
            )

            role_counter[role] += 1

            characters += len(content)

            word_count = len(content.split())

            words += word_count

            longest_message = max(
                longest_message,
                word_count,
            )

        total_messages = len(messages)

        average_words = (
            round(words / total_messages, 2)
            if total_messages
            else 0
        )

        return {
            "messages": total_messages,
            "characters": characters,
            "words": words,
            "average_words": average_words,
            "longest_message_words": longest_message,
            "user_messages": role_counter.get(
                "user",
                0,
            ),
            "assistant_messages": role_counter.get(
                "assistant",
                0,
            ),
            "system_messages": role_counter.get(
                "system",
                0,
            ),
        }

    # --------------------------------------------------

    def summary(
        self,
        messages: list[dict],
    ) -> str:

        stats = self.analyze(messages)

        return (
            f"Messages: {stats['messages']} | "
            f"Words: {stats['words']} | "
            f"Characters: {stats['characters']}"
        )


chat_analytics_service = ChatAnalyticsService()