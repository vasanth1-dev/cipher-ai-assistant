import json
import os

from collections import deque
from datetime import datetime

from core.logger import logger


class HistoryService:

    def __init__(self, limit=200):

        self.limit = limit

        self.file = "data/history.json"

        os.makedirs("data", exist_ok=True)

        self.history = deque(
            maxlen=self.limit,
        )

        self._load()

    # ------------------------------------------------ #
    # File Handling
    # ------------------------------------------------ #

    def _load(self):

        if not os.path.exists(self.file):

            self._save()

            return

        try:

            with open(
                self.file,
                "r",
                encoding="utf-8",
            ) as f:

                data = json.load(f)

                if isinstance(data, list):

                    self.history.extend(
                        data[-self.limit:]
                    )

        except Exception as e:

            logger.exception(e)

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

        except Exception as e:

            logger.exception(e)

    # ------------------------------------------------ #
    # Add Conversation
    # ------------------------------------------------ #

    def add(self, command, response):

        item = {
            "timestamp": datetime.now().isoformat(
                timespec="seconds"
            ),
            "command": command,
            "response": response,
        }

        self.history.append(item)

        self._save()

        logger.info("[HISTORY] Conversation saved.")

    # ------------------------------------------------ #
    # Get History
    # ------------------------------------------------ #

    def last(self):

        if not self.history:
            return None

        return self.history[-1]

    def all(self):

        return list(self.history)

    def recent(self, count=10):

        if count <= 0:
            return []

        return list(self.history)[-count:]

    # ------------------------------------------------ #
    # Search
    # ------------------------------------------------ #

    def search(self, keyword):

        keyword = keyword.lower()

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

        self._save()

        logger.info("[HISTORY] Cleared.")

    def is_empty(self):

        return len(self.history) == 0


history_service = HistoryService()