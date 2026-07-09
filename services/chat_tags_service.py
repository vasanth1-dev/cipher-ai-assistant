from __future__ import annotations

import json
from pathlib import Path


class ChatTagsService:
    """
    Stores user-defined tags for chat sessions.

    Example:
        session_001 -> ["python", "ollama", "linux"]
    """

    def __init__(self):

        self._path = Path("data/chat_tags.json")
        self._path.parent.mkdir(parents=True, exist_ok=True)

        self._tags = self._load()

    # --------------------------------------------------

    def _load(self):

        if not self._path.exists():
            return {}

        try:

            with open(
                self._path,
                "r",
                encoding="utf-8",
            ) as f:

                return json.load(f)

        except Exception:
            return {}

    # --------------------------------------------------

    def _save(self):

        with open(
            self._path,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                self._tags,
                f,
                indent=4,
                ensure_ascii=False,
                sort_keys=True,
            )

    # --------------------------------------------------

    def add_tag(
        self,
        session_id: str,
        tag: str,
    ):

        tag = tag.strip().lower()

        if not tag:
            return

        tags = self._tags.setdefault(session_id, [])

        if tag not in tags:
            tags.append(tag)
            tags.sort()
            self._save()

    # --------------------------------------------------

    def remove_tag(
        self,
        session_id: str,
        tag: str,
    ):

        tag = tag.strip().lower()

        if session_id not in self._tags:
            return

        if tag in self._tags[session_id]:
            self._tags[session_id].remove(tag)

            if not self._tags[session_id]:
                del self._tags[session_id]

            self._save()

    # --------------------------------------------------

    def get_tags(
        self,
        session_id: str,
    ):

        return list(
            self._tags.get(session_id, [])
        )

    # --------------------------------------------------

    def has_tag(
        self,
        session_id: str,
        tag: str,
    ) -> bool:

        return (
            tag.strip().lower()
            in self._tags.get(session_id, [])
        )

    # --------------------------------------------------

    def sessions_with_tag(
        self,
        tag: str,
    ):

        tag = tag.strip().lower()

        return [
            session_id
            for session_id, tags in self._tags.items()
            if tag in tags
        ]

    # --------------------------------------------------

    def clear_session(
        self,
        session_id: str,
    ):

        if session_id in self._tags:
            del self._tags[session_id]
            self._save()


chat_tags_service = ChatTagsService()