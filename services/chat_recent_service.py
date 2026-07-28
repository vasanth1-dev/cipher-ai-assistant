from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


class ChatRecentService:
    """
    Tracks recently opened chat sessions.

    This service is independent of chat history and
    is intended for future "Recent Chats" features.
    """

    MAX_RECENT = 20

    def __init__(
       self,
    ) -> None:

        self._file = Path("data/chat_recent.json")
        self._file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._recent = self._load()

    # --------------------------------------------------

    def _load(self):

        if not self._file.exists():
            return []

        try:

            with open(
                self._file,
                "r",
                encoding="utf-8",
            ) as file:

                return json.load(file)

        except Exception:
            return []

    # --------------------------------------------------

    def _save(self):

        with open(
            self._file,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                self._recent,
                file,
                indent=4,
                ensure_ascii=False,
            )

    # --------------------------------------------------

    def touch(
        self,
        session_id: str,
        title: str,
    ):

        self._recent = [
            item
            for item in self._recent
            if item["session_id"] != session_id
        ]

        self._recent.insert(
            0,
            {
                "session_id": session_id,
                "title": title,
                "opened_at": datetime.now().isoformat(),
            },
        )

        self._recent = self._recent[: self.MAX_RECENT]

        self._save()

    # --------------------------------------------------

    def list(self):

        return list(self._recent)

    # --------------------------------------------------

    def remove(
        self,
        session_id: str,
    ):

        self._recent = [
            item
            for item in self._recent
            if item["session_id"] != session_id
        ]

        self._save()

    # --------------------------------------------------

    def clear(self):

        self._recent.clear()
        self._save()

    # --------------------------------------------------

    def count(self):

        return len(self._recent)


chat_recent_service = ChatRecentService()