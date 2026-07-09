from __future__ import annotations

from collections import deque


class ChatContextService:
    """
    Maintains the active conversation context.

    This service is intentionally independent from the UI
    and the LLM. It simply stores and manages the current
    conversation context.
    """

    def __init__(self):

        self.clear()

    # --------------------------------------------------

    def add(
        self,
        role: str,
        content: str,
    ):

        self._messages.append(
            {
                "role": role,
                "content": content,
            }
        )

    # --------------------------------------------------

    def extend(
        self,
        messages: list[dict],
    ):

        for message in messages:
            self.add(
                message.get("role", "assistant"),
                message.get("content", ""),
            )

    # --------------------------------------------------

    def messages(self) -> list[dict]:

        return list(self._messages)

    # --------------------------------------------------

    def last(
        self,
    ) -> dict | None:

        if not self._messages:
            return None

        return self._messages[-1]

    # --------------------------------------------------

    def limit(
        self,
        maximum_messages: int,
    ):

        while len(self._messages) > maximum_messages:
            self._messages.popleft()

    # --------------------------------------------------

    def remove_last(self):

        if self._messages:
            self._messages.pop()

    # --------------------------------------------------

    def clear(self):

        self._messages = deque()

    # --------------------------------------------------

    def count(self) -> int:

        return len(self._messages)

    # --------------------------------------------------

    def empty(self) -> bool:

        return len(self._messages) == 0


chat_context_service = ChatContextService()