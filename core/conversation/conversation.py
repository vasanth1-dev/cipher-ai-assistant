from dataclasses import dataclass, field
from datetime import datetime
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
        default_factory=lambda: datetime.now().isoformat()
    )

    updated_at: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )

    pinned: bool = False

    messages: list = field(
        default_factory=list
    )

    def add_message(
        self,
        sender: str,
        text: str,
    ):

        self.messages.append({

            "sender": sender,

            "text": text,

            "time": datetime.now().isoformat(),

        })

        # Automatically generate the title
        # from the first user message.
        if (
            self.title == "New Chat"
            and sender == "You"
        ):
            
            title = text.strip()

            if len(title) > 40:
                title = title[:40].rstrip() + "..."

            self.title = title

        self.updated_at = datetime.now().isoformat()

    def rename(
        self,
        title: str,
    ):

        self.title = title

        self.updated_at = datetime.now().isoformat()

    def pin(self):

        self.pinned = True

    def unpin(self):

        self.pinned = False