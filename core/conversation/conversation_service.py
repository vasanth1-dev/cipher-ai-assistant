from typing import Final

from core.conversation.conversation import Conversation
from core.conversation.conversation_manager import ConversationManager

USER_ROLE: Final[str] = "You"
ASSISTANT_ROLE: Final[str] = "Cipher"
SYSTEM_ROLE: Final[str] = "System"

class ConversationService:
    """
    Public API for the Conversation System.

    The GUI should use this service instead of
    talking directly to ConversationManager.
    """

    def __init__(
        self,
        manager: ConversationManager | None = None,
    ):
        self.manager = manager or ConversationManager()

    # --------------------------------------------------
    # Conversation
    # --------------------------------------------------

    def new_chat(
        self, 
        title: str = "New Chat"
    ) -> Conversation:

        return self.manager.create(title)

    def get_current(
        self
    ) -> Conversation | None:

        return self.manager.get_current()

    def get_all(
        self,
    ) -> list[Conversation]:

        return self.manager.get_all()

    def set_current(
        self,
        conversation_id: str,
    ) -> Conversation | None:

        return self.manager.set_current(
            conversation_id
        )

    # --------------------------------------------------
    # Messages
    # --------------------------------------------------

    def add_message(
        self,
        sender: str,
        text: str,
    ) -> None:

        if not isinstance(text, str):
            return

        text = text.strip()

        if not text:
            return

        conversation = (
            self.manager.get_current()
            or self.manager.create()
        )

        conversation.add_message(
            sender,
            text,
        )

        try:
            self.manager.save_current()
        except Exception:
            raise

    def add_user_message(
        self,
        text: str,
    ) -> None:

        self.add_message(
            USER_ROLE,
            text,
        )

    def add_assistant_message(
        self,
        text: str,
    ) -> None:

        self.add_message(
            ASSISTANT_ROLE,
            text,
        )

    def add_system_message(
        self,
        text: str,
    ) -> None:

        self.add_message(
            SYSTEM_ROLE,
            text,
        )

    # --------------------------------------------------
    # Conversation Actions
    # --------------------------------------------------

    def rename(
        self, 
        conversation_id: str, 
        title: str,
    ) ->None:

        self.manager.rename(
            conversation_id,
            title,
        )

    def delete(
        self, 
        conversation_id: str,
    ) -> None:

        self.manager.delete(
            conversation_id,
        )

    def pin(
        self, 
        conversation_id: str,
    ) -> None:

        self.manager.pin(
            conversation_id,
        )

    def unpin(
        self, 
        conversation_id: str,
    ) -> None:

        self.manager.unpin(
            conversation_id,
        )

    def search(
        self,
        text: str,
    ) -> list[Conversation]:

        if not text.strip():
            return []

        return self.manager.search(text)

# Create in application_bootstrap.py or run_gui.py

conversation_service = ConversationService()
