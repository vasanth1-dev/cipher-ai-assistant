import json
from pathlib import Path

from core.conversation.conversation import Conversation


class ConversationStorage:
    """
    Handles saving and loading conversations.
    """

    def __init__(self):

        self.data_dir = Path("data/conversations")

        self.data_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    # -----------------------------------------

    def save(
        self,
        conversation: Conversation,
    ):

        path = self.data_dir / f"{conversation.id}.json"

        with open(
            path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(

                conversation.__dict__,

                file,

                indent=4,

                ensure_ascii=False,

            )

    # -----------------------------------------

    def load(
        self,
        conversation_id: str,
    ):

        path = self.data_dir / f"{conversation_id}.json"

        if not path.exists():

            return None

        with open(
            path,
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

        return Conversation(**data)

    # -----------------------------------------

    def delete(
        self,
        conversation_id: str,
    ):

        path = self.data_dir / f"{conversation_id}.json"

        if path.exists():

            path.unlink()

    # -----------------------------------------

    def load_all(self):

        conversations = []

        for file in self.data_dir.glob("*.json"):

            with open(
                file,
                "r",
                encoding="utf-8",
            ) as f:

                data = json.load(f)

                conversations.append(
                    Conversation(**data)
                )

        conversations.sort(

            key=lambda c: c.updated_at,

            reverse=True,

        )

        return conversations