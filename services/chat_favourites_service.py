from __future__ import annotations

import json
from pathlib import Path


class ChatFavoritesService:
    """
    Manages favorite/bookmarked messages.

    Favorites are stored independently from chat history.
    """

    def __init__(self):

        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)

        self.file = self.data_dir / "favorites.json"

        self._favorites = self._load()

    # --------------------------------------------------

    def _load(self):

        if not self.file.exists():
            return []

        try:

            with open(
                self.file,
                "r",
                encoding="utf-8",
            ) as f:

                return json.load(f)

        except Exception:
            return []

    # --------------------------------------------------

    def _save(self):

        with open(
            self.file,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                self._favorites,
                f,
                indent=4,
                ensure_ascii=False,
            )

    # --------------------------------------------------

    def add(
        self,
        session_id: str,
        role: str,
        content: str,
    ):

        item = {
            "session_id": session_id,
            "role": role,
            "content": content,
        }

        if item in self._favorites:
            return

        self._favorites.append(item)

        self._save()

    # --------------------------------------------------

    def remove(
        self,
        session_id: str,
        content: str,
    ):

        self._favorites = [
            item
            for item in self._favorites
            if not (
                item["session_id"] == session_id
                and item["content"] == content
            )
        ]

        self._save()

    # --------------------------------------------------

    def list(self):

        return list(self._favorites)

    # --------------------------------------------------

    def clear(self):

        self._favorites.clear()
        self._save()

    # --------------------------------------------------

    def count(self):

        return len(self._favorites)


chat_favorites_service = ChatFavoritesService()