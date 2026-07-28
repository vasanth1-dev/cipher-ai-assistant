from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ChatMessage:
    """
    Represents a single message in the conversation.
    """

    role: str
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    message_id: str = ""
    status: str = "completed"
    metadata: dict = field(default_factory=dict)


class ChatSession:
    """
    Stores the current conversation independently of the UI.

    This class intentionally contains no rendering code and no
    LLM logic. It only manages conversation state.
    """

    def __init__(
       self,
    ) -> None:
        self.clear()

    # ---------------------------------------------------------

    def add_user_message(self, text: str) -> ChatMessage:
        message = ChatMessage(
            role="user",
            content=text,
        )

        self._messages.append(message)
        return message

    # ---------------------------------------------------------

    def add_assistant_message(self, text: str) -> ChatMessage:
        message = ChatMessage(
            role="assistant",
            content=text,
        )

        self._messages.append(message)
        return message

    # ---------------------------------------------------------

    def add_system_message(self, text: str) -> ChatMessage:
        message = ChatMessage(
            role="system",
            content=text,
        )

        self._messages.append(message)
        return message

    # ---------------------------------------------------------

    def messages(self) -> list[ChatMessage]:
        return list(self._messages)

    # ---------------------------------------------------------

    def last_message(self) -> ChatMessage | None:
        if not self._messages:
            return None

        return self._messages[-1]

    # ---------------------------------------------------------

    def count(self) -> int:
        return len(self._messages)

    # ---------------------------------------------------------

    def is_empty(self) -> bool:
        return len(self._messages) == 0

    # ---------------------------------------------------------

    def clear(self):
        self._messages: list[ChatMessage] = []

    # ---------------------------------------------------------

    def to_openai_messages(self) -> list[dict]:
        """
        Returns conversation in a generic LLM-friendly format.
        """

        return [
            {
                "role": message.role,
                "content": message.content,
            }
            for message in self._messages
        ]