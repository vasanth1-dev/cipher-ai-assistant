from __future__ import annotations

import json
from pathlib import Path


class ChatIndexService:
    """
    Maintains an index of chat sessions.

    The index provides a lightweight lookup for
    conversation metadata without opening every
    history file.
    """

    INDEX_FILE = Path("data/chat_index.json")

    def __init__(self):

        self.INDEX_FILE.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._index = self._load()

    # --------------------------------------------------

    def _load(self):

        if not self.INDEX_FILE.exists():
            return {}

        try:

            with open(
                self.INDEX_FILE,
                "r",
                encoding="utf-8",
            ) as file:

                return json.load(file)

        except Exception:
            return {}

    # --------------------------------------------------

    def _save(self):

        with open(
            self.INDEX_FILE,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                self._index,
                file,
                indent=4,
                ensure_ascii=False,
                sort_keys=True,
            )

    # --------------------------------------------------

    def add(
        self,
        session_id: str,
        title: str,
    ):

        self._index[session_id] = {
            "title": title,
        }

        self._save()

    # --------------------------------------------------

    def update(
        self,
        session_id: str,
        **fields,
    ):

        if session_id not in self._index:
            self._index[session_id] = {}

        self._index[session_id].update(fields)

        self._save()

    # --------------------------------------------------

    def remove(
        self,
        session_id: str,
    ):

        if session_id in self._index:

            del self._index[session_id]

            self._save()

    # --------------------------------------------------

    def get(
        self,
        session_id: str,
    ):

        return dict(
            self._index.get(session_id, {})
        )

    # --------------------------------------------------

    def list(self):

        return dict(self._index)

    # --------------------------------------------------

    def clear(self):

        self._index.clear()
        self._save()


chat_index_service = ChatIndexService()