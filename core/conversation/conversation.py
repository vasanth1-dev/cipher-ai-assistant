from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Any
import uuid


@dataclass
class Conversation:
    """
    Represents one chat conversation.
    """

    title: str = "New Chat"

    id: str = field(
        default_factory=lambda: str(uuid.uuid4())
    )

    created_at: str = field(
        default_factory=lambda: datetime.now(UTC).isoformat()
    )

    updated_at: str = field(
        default_factory=lambda: datetime.now(UTC).isoformat()
    )

    pinned: bool = False

    messages: list[dict[str, Any]] = field(
        default_factory=list
    )

    def add_message(
        self,
        sender: str,
        text: str,
    ) -> None:

        if not sender.strip() or not text.strip():
            return

        self.messages.append(
            {
                "sender": sender,
                "text": text,
                "time": datetime.now(UTC).isoformat(),
            }
        )

        # Automatically generate the title
        # from the first user message.
        if (
            self.title == "New Chat"
            and sender == "You"
            and text.strip()
        ):
            
            title = " ".join(text.split())

            title = title[:40].rstrip()

            if len(title) == 40:
                title += "..."

            self.title = title or "New Chat"

        self.updated_at = datetime.now(UTC).isoformat()

    def rename(
        self,
        title: str,
    ) -> None:

        title = " ".join(title.split())

        if title:
            self.title = title

        self.updated_at = datetime.now(UTC).isoformat()

        self.updated_at = datetime.now().isoformat()

    def pin(self) -> None:

        self.pinned = True
        self.updated_at = datetime.now(UTC).isoformat()

    def unpin(self) -> None:

        self.pinned = False
        self.updated_at = datetime.now(UTC).isoformat()