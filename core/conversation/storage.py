import json
import tempfile
from pathlib import Path

from core.conversation.conversation import Conversation


class ConversationStorage:
    """
    Handles saving and loading conversations.
    """

    def __init__(
       self,
    ) -> None:

        self.data_dir = Path("data") / "conversations"

        self.data_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    # -----------------------------------------

    def save(
        self,
        conversation: Conversation,
    ) -> None:

        path = self.data_dir / f"{conversation.id}.json"

        temp_file = None

        try:
            with tempfile.NamedTemporaryFile(
                "w",
                encoding="utf-8",
                dir=self.data_dir,
                delete=False,
            ) as file:

                temp_file = Path(file.name)

                json.dump(
                    vars(conversation),
                    file,
                    indent=4,
                    ensure_ascii=False,
                )

            temp_file.replace(path)

        except Exception:
            if temp_file and temp_file.exists():
                temp_file.unlink()
            raise

    # -----------------------------------------

    def load(
        self,
        conversation_id: str,
    ) -> Conversation | None:

        path = self.data_dir / f"{conversation_id}.json"

        if not path.exists():

            return None

        try:
            with open(
                path,
                "r",
                encoding="utf-8",
            ) as file:

                data = json.load(file)

            return Conversation(**data)

        except (
            json.JSONDecodeError,
            TypeError,
            ValueError,
        ):
            return None

    # -----------------------------------------

    def delete(
        self,
        conversation_id: str,
    ) -> None:

        path = self.data_dir / f"{conversation_id}.json"

        if path.exists():

            path.unlink(missing_ok=True)

    # -----------------------------------------

    def load_all(
        self,
    ) -> list[Conversation]:

        conversations = []

        for file in self.data_dir.glob("*.json"):

            try:

                with open(
                    file,
                    "r",
                    encoding="utf-8",
                ) as f:

                    data = json.load(f)

                conversations.append(
                    Conversation(**data)
                )

            except (
                json.JSONDecodeError,
                TypeError,
                ValueError,
            ):
                continue

        conversations.sort(

            key=lambda c: (
                c.updated_at,
                c.created_at,
            ),

            reverse=True,

        )

        return conversations