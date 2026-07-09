"""
Cipher v2
Conversation Manager

Maintains conversation state for the current Cipher session.

Features
--------
- Conversation history
- Configurable history limit
- Session reset
- Message metadata
- Context export
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import Any

from core.logger import logger


@dataclass
class ConversationMessage:
    """
    Represents a single conversation message.
    """

    role: str
    content: str
    timestamp: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )
    metadata: dict[str, Any] = field(default_factory=dict)


class ConversationManager:
    """
    Stores conversation history for the current session.
    """

    def __init__(self, max_messages: int = 100):
        self.max_messages = max(1, max_messages)
        self._messages: deque[ConversationMessage] = deque(
            maxlen=self.max_messages
        )

    # --------------------------------------------------
    # Messages
    # --------------------------------------------------

    def add_user_message(
        self,
        text: str,
        **metadata,
    ) -> None:
        self._add(
            role="user",
            content=text,
            metadata=metadata,
        )

    def add_assistant_message(
        self,
        text: str,
        **metadata,
    ) -> None:
        self._add(
            role="assistant",
            content=text,
            metadata=metadata,
        )

    def add_system_message(
        self,
        text: str,
        **metadata,
    ) -> None:
        self._add(
            role="system",
            content=text,
            metadata=metadata,
        )

    def _add(
        self,
        role: str,
        content: str,
        metadata: dict[str, Any],
    ) -> None:
        message = ConversationMessage(
            role=role,
            content=content,
            metadata=metadata,
        )

        self._messages.append(message)

        logger.debug(
            "Conversation message added (%s).",
            role,
        )

    # --------------------------------------------------
    # Retrieval
    # --------------------------------------------------

    def history(self) -> list[dict[str, Any]]:
        """
        Return the complete conversation history.
        """
        return [
            asdict(message)
            for message in self._messages
        ]

    def recent(
        self,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        """
        Return the most recent messages.
        """
        limit = max(1, limit)

        return [
            asdict(message)
            for message in list(self._messages)[-limit:]
        ]

    def context(
        self,
        limit: int = 20,
    ) -> list[dict[str, str]]:
        """
        Return conversation context suitable for LLMs.
        """
        limit = max(1, limit)

        return [
            {
                "role": message.role,
                "content": message.content,
            }
            for message in list(self._messages)[-limit:]
        ]

    # --------------------------------------------------
    # Session
    # --------------------------------------------------

    def clear(self) -> None:
        """
        Clear the current conversation.
        """
        self._messages.clear()

        logger.info(
            "Conversation history cleared."
        )

    def count(self) -> int:
        """
        Return the number of stored messages.
        """
        return len(self._messages)

    def empty(self) -> bool:
        """
        Return True if there are no messages.
        """
        return len(self._messages) == 0