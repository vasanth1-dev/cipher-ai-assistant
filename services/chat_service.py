import json
import os
from datetime import datetime

from core.logger import logger


class ChatService:

    def __init__(self):

        self.chat_dir = "data/chats"

        os.makedirs(
            self.chat_dir,
            exist_ok=True,
        )

        self.current_chat = None

        self.create_chat()

    # ------------------------------------------------ #
    # Chat ID
    # ------------------------------------------------ #

    def _generate_chat_id(self):

        files = [

            file

            for file in os.listdir(
                self.chat_dir
            )

            if file.endswith(".json")

        ]

        if not files:
            return "chat_001"

        numbers = []

        for file in files:

            try:

                number = int(
                    file.replace(
                        "chat_",
                        "",
                    ).replace(
                        ".json",
                        "",
                    )
                )

                numbers.append(number)

            except Exception:
                pass

        if not numbers:
            return "chat_001"

        return f"chat_{max(numbers)+1:03d}"

    # ------------------------------------------------ #
    # Create Chat
    # ------------------------------------------------ #

    def create_chat(self):

        chat_id = self._generate_chat_id()

        data = {

            "chat_id": chat_id,

            "title": "New Chat",

            "created_at": datetime.now().isoformat(
                timespec="seconds"
            ),

            "updated_at": datetime.now().isoformat(
                timespec="seconds"
            ),

            "messages": []

        }

        self._save(chat_id, data)

        self.current_chat = chat_id

        logger.info(
            f"[CHAT] Created {chat_id}"
        )

        return chat_id

    # ------------------------------------------------ #
    # Save
    # ------------------------------------------------ #

    def _save(self, chat_id, data):

        path = os.path.join(
            self.chat_dir,
            f"{chat_id}.json",
        )

        with open(
            path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False,
            )

    # ------------------------------------------------ #
    # Load
    # ------------------------------------------------ #

    def load_chat(self, chat_id):

        path = os.path.join(
            self.chat_dir,
            f"{chat_id}.json",
        )

        if not os.path.exists(path):
            return None

        with open(
            path,
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

        self.current_chat = chat_id

        return data

    # ------------------------------------------------ #
    # Add Message
    # ------------------------------------------------ #

    def add_message(
        self,
        role,
        content,
    ):

        if not self.current_chat:
            return

        data = self.load_chat(
            self.current_chat
        )

        if data is None:
            return

        data["messages"].append({

            "role": role,

            "content": content,

            "timestamp": datetime.now().isoformat(
                timespec="seconds"
            )

        })

        if (

            data["title"]
            == "New Chat"

            and role == "user"

        ):

            data["title"] = content[:40]

        data["updated_at"] = datetime.now().isoformat(
            timespec="seconds"
        )

        self._save(
            self.current_chat,
            data,
        )

    # ------------------------------------------------ #
    # List Chats
    # ------------------------------------------------ #

    def all_chats(self):

        chats = []

        for file in os.listdir(
            self.chat_dir
        ):

            if not file.endswith(".json"):
                continue

            try:

                with open(

                    os.path.join(
                        self.chat_dir,
                        file,
                    ),

                    "r",
                    encoding="utf-8",

                ) as f:

                    chats.append(
                        json.load(f)
                    )

            except Exception as e:

                logger.exception(e)

        chats.sort(

            key=lambda x: x["updated_at"],

            reverse=True,

        )

        return chats

    # ------------------------------------------------ #
    # Current Chat
    # ------------------------------------------------ #

    def current(self):

        return self.current_chat


chat_service = ChatService()