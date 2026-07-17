from core.conversation.conversation_manager import (
    ConversationManager,
)


class ConversationService:
    """
    Public API for the Conversation System.

    The GUI should use this service instead of
    talking directly to ConversationManager.
    """

    def __init__(self):

        self.manager = ConversationManager()

    # --------------------------------------------------
    # Conversation
    # --------------------------------------------------

    def new_chat(self, title="New Chat"):

        return self.manager.create(title)

    def get_current(self):

        return self.manager.get_current()

    def get_all(self):

        return self.manager.get_all()

    def set_current(self, conversation_id):

        return self.manager.set_current(
            conversation_id
        )

    # --------------------------------------------------
    # Messages
    # --------------------------------------------------

    def add_user_message(self, text):

        conversation = self.manager.get_current()

        if conversation is None:

            conversation = self.manager.create()

        conversation.add_message(
            "You",
            text,
        )

        self.manager.save_current()

    def add_assistant_message(self, text):

        conversation = self.manager.get_current()

        if conversation is None:

            conversation = self.manager.create()

        conversation.add_message(
            "Cipher",
            text,
        )

        self.manager.save_current()

    def add_system_message(self, text):

        conversation = self.manager.get_current()

        if conversation is None:

            conversation = self.manager.create()

        conversation.add_message(
            "System",
            text,
        )

        self.manager.save_current()

    # --------------------------------------------------
    # Conversation Actions
    # --------------------------------------------------

    def rename(self, conversation_id, title):

        self.manager.rename(
            conversation_id,
            title,
        )

    def delete(self, conversation_id):

        self.manager.delete(
            conversation_id,
        )

    def pin(self, conversation_id):

        self.manager.pin(
            conversation_id,
        )

    def unpin(self, conversation_id):

        self.manager.unpin(
            conversation_id,
        )

    def search(self, text):

        return self.manager.search(text)


conversation_service = ConversationService()