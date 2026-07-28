import json

from pathlib import Path
from collections import deque
from datetime import datetime

from core.logger import logger


class HistoryService:

    def __init__(self, limit=200):

        self.limit = limit

        self.file = Path(
            "data/history.json"
        )

        self.file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.history = deque(
            maxlen=self.limit,
        )

        self._load()

    # ------------------------------------------------ #
    # File Handling
    # ------------------------------------------------ #

    def _load(self):

        if not self.file.exists():

            self._commit()

            return

        try:

            with open(
                self.file,
                "r",
                encoding="utf-8",
            ) as f:

                data = json.load(f)

                if isinstance(data, list):

                    for item in data[-self.limit:]:

                        if (
                            isinstance(item, dict)
                            and "command" in item
                            and "response" in item
                        ):

                            self.history.append(item)

                            logger.info(
                                f"[HISTORY] Loaded {len(self.history)}"
                            )

        except Exception as e:

            logger.exception(
                f"[HISTORY] Failed to load history: {e}"
            )

    def _save(self):

        try:

            with open(
                self.file,
                "w",
                encoding="utf-8",
            ) as f:

                json.dump(
                    list(self.history),
                    f,
                    indent=4,
                    ensure_ascii=False,
                )

                logger.debug(
                    "[HISTORY] Saved successfully."
                )

        except Exception as e:

            logger.exception(
                f"[HISTORY] Failed to save history: {e}"
            )

    def _normalize_text(
        self,
        text: str,
    ) -> str:
        return str(text).strip()
    
    def _commit(
        self,
    ) -> None:

        self._save()
    
    def _create_history_item(
        self,
        command: str,
        response: str,
    ) -> dict:

        return {

            "timestamp": datetime.now().isoformat(
                timespec="seconds",
            ),

            "command": command,

            "response": response,

        }

    # ------------------------------------------------ #
    # Add Conversation
    # ------------------------------------------------ #

    def add(
        self, 
        command: str, 
        response: str,
    ) -> None:

        command = self._normalize_text(command)
        response = self._normalize_text(response)

        if not command or not response:
            return

        item = self._create_history_item(
            command,
            response,
        )


        self.history.append(item)

        self._commit()

        logger.info("[HISTORY] Conversation saved.")

    # ------------------------------------------------ #
    # Get History
    # ------------------------------------------------ #

    def last(
        self,
    ) -> dict | None:

        if not self.history:
            return None

        return self.history[-1]

    def all(self):

        return list(self.history)

    def recent(
        self, 
        count: int = 10,
    ) -> list[dict]:

        if count <= 0:
            return []

        return list(self.history)[-count:]

    # ------------------------------------------------ #
    # Search
    # ------------------------------------------------ #

    def search(self, keyword):

        keyword = self._normalize_text(keyword).lower()

        if not keyword:
            return []

        return [

            item

            for item in self.history

            if keyword in item["command"].lower()
            or keyword in item["response"].lower()

        ]

    # ------------------------------------------------ #
    # Utilities
    # ------------------------------------------------ #

    def count(self):

        return len(self.history)

    def clear(self):

        self.history.clear()

        self._commit()

        logger.info("[HISTORY] Cleared.")

    def delete_last(self):

        if not self.history:
            return False

        self.history.pop()

        self._commit()

        logger.info(
            "[HISTORY] Last conversation deleted."
        )

        return True

    def is_empty(self):

        return len(self.history) == 0


history_service = HistoryService()