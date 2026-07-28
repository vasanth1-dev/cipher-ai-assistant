from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


class ChatBookmarkService:
    """
    Manages bookmarks for conversations.

    A bookmark references a specific message in a
    conversation without modifying the conversation
    itself.
    """

     def __init__(
       self,
    ) -> None:

        self._file = Path("data/chat_bookmarks.json")
        self._file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._bookmarks = self._load()

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
                self._bookmarks,
                file,
                indent=4,
                ensure_ascii=False,
            )

    # --------------------------------------------------

    def add(
        self,
        session_id: str,
        message_index: int,
        title: str,
    ):

        bookmark = {
            "session_id": session_id,
            "message_index": message_index,
            "title": title,
            "created_at": datetime.now().isoformat(),
        }

        if bookmark not in self._bookmarks:
            self._bookmarks.append(bookmark)
            self._save()

    # --------------------------------------------------

    def remove(
        self,
        session_id: str,
        message_index: int,
    ):

        self._bookmarks = [
            bookmark
            for bookmark in self._bookmarks
            if not (
                bookmark["session_id"] == session_id
                and bookmark["message_index"] == message_index
            )
        ]

        self._save()

    # --------------------------------------------------

    def list(self):

        return list(self._bookmarks)

    # --------------------------------------------------

    def session_bookmarks(
        self,
        session_id: str,
    ):

        return [
            bookmark
            for bookmark in self._bookmarks
            if bookmark["session_id"] == session_id
        ]

    # --------------------------------------------------

    def clear(self):

        self._bookmarks.clear()
        self._save()

    # --------------------------------------------------

    def count(self):

        return len(self._bookmarks)


chat_bookmark_service = ChatBookmarkService()