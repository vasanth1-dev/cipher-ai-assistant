from core.conversation.conversation import Conversation
from core.conversation.storage import ConversationStorage


class ConversationManager:
    """
    Manages all conversations.
    """

    def __init__(
       self,
    ) -> None:

        self.storage = ConversationStorage()

        self.conversations = self.storage.load_all()

        self.current = (
            self.conversations[0]
            if self.conversations
            else None
        )

    # -------------------------------------------------

    def create(self, title= "New Chat"):

        conversation = Conversation(title=title)

        self.conversations.insert(
            0,
            conversation,
        )

        self.current = conversation

        self.storage.save(conversation)

        return conversation

    # -------------------------------------------------

    def get_all(self):

        return self.conversations

    # -------------------------------------------------

    def get_current(self) -> Conversation | None:

        return self.current

    # -------------------------------------------------

    def set_current(self, conversation_id):

        for conversation in self.conversations:

            if conversation.id == conversation_id:

                self.current = conversation

                return conversation

        return None

    # -------------------------------------------------

    def save_current(self):

        if self.current is None:

            return

        self.storage.save(self.current)

    # -------------------------------------------------

    def rename(
        self,
        conversation_id,
        title,
    ):

        conversation = self.get_by_id(
            conversation_id
        )

        if conversation is None:

            return

        conversation.rename(title)

        self.storage.save(conversation)

    # -------------------------------------------------

    def delete(
        self,
        conversation_id,
    ):

        self.storage.delete(conversation_id)

        self.conversations = [

            c

            for c in self.conversations

            if c.id != conversation_id

        ]

        if self.conversations:
            self.current = self.conversations[0]
        else:
            self.current = None

    # -------------------------------------------------

    def pin(
        self,
        conversation_id,
    ):

        conversation = self.get_by_id(
            conversation_id
        )

        if conversation:

            conversation.pin()

            self.storage.save(conversation)

    # -------------------------------------------------

    def unpin(
        self,
        conversation_id,
    ):

        conversation = self.get_by_id(
            conversation_id
        )

        if conversation:

            conversation.unpin()

            self.storage.save(conversation)

    # -------------------------------------------------

    def search(
        self,
        text,
    ):

        text = text.lower()

        return [

            conversation

            for conversation in self.conversations

            if text in (conversation.title or "").lower()

        ]

    def get_by_id(self, conversation_id):
        for conversation in self.conversations:
            if conversation.id == conversation_id:
                return conversation
        return None