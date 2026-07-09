from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass
class ChatSession:

    session_id: str
    title: str
    created_at: datetime
    updated_at: datetime
    message_count: int = 0
    metadata: dict = field(default_factory=dict)


class ChatSessionService:
    """
    Manages chat session metadata.

    This service only tracks sessions.
    Message persistence is handled separately by
    chat_history_service.
    """

    def __init__(self):

        self._sessions: dict[str, ChatSession] = {}

    # --------------------------------------------------

    def create(self, title: str = "New Chat") -> ChatSession:

        now = datetime.now()

        session = ChatSession(
            session_id=str(uuid4()),
            title=title,
            created_at=now,
            updated_at=now,
        )

        self._sessions[session.session_id] = session

        return session

    # --------------------------------------------------

    def get(self, session_id: str) -> ChatSession | None:

        return self._sessions.get(session_id)

    # --------------------------------------------------

    def list(self) -> list[ChatSession]:

        return sorted(
            self._sessions.values(),
            key=lambda s: s.updated_at,
            reverse=True,
        )

    # --------------------------------------------------

    def rename(
        self,
        session_id: str,
        title: str,
    ) -> bool:

        session = self.get(session_id)

        if session is None:
            return False

        session.title = title
        session.updated_at = datetime.now()

        return True

    # --------------------------------------------------

    def increment_message_count(
        self,
        session_id: str,
    ):

        session = self.get(session_id)

        if session is None:
            return

        session.message_count += 1
        session.updated_at = datetime.now()

    # --------------------------------------------------

    def delete(
        self,
        session_id: str,
    ) -> bool:

        if session_id not in self._sessions:
            return False

        del self._sessions[session_id]
        return True

    # --------------------------------------------------

    def clear(self):

        self._sessions.clear()


chat_session_service = ChatSessionService()