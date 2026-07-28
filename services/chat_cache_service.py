from __future__ import annotations

import json
from pathlib import Path


class ChatCacheService:
    """
    Lightweight key-value cache for chat-related data.

    This service is intentionally generic so it can be used for:
    - Recent conversations
    - Search cache
    - Model responses
    - Session state
    - Temporary UI data
    """

    CACHE_FILE = Path("data/chat_cache.json")

     def __init__(
       self,
    ) -> None:

        self.CACHE_FILE.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._cache = self._load()

    # --------------------------------------------------

    def _load(self):

        if not self.CACHE_FILE.exists():
            return {}

        try:

            with open(
                self.CACHE_FILE,
                "r",
                encoding="utf-8",
            ) as file:

                return json.load(file)

        except Exception:
            return {}

    # --------------------------------------------------

    def _save(self):

        with open(
            self.CACHE_FILE,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                self._cache,
                file,
                indent=4,
                ensure_ascii=False,
                sort_keys=True,
            )

    # --------------------------------------------------

    def get(
        self,
        key: str,
        default=None,
    ):

        return self._cache.get(
            key,
            default,
        )

    # --------------------------------------------------

    def set(
        self,
        key: str,
        value,
    ):

        self._cache[key] = value
        self._save()

    # --------------------------------------------------

    def remove(
        self,
        key: str,
    ):

        if key in self._cache:

            del self._cache[key]
            self._save()

    # --------------------------------------------------

    def contains(
        self,
        key: str,
    ) -> bool:

        return key in self._cache

    # --------------------------------------------------

    def clear(self):

        self._cache.clear()
        self._save()

    # --------------------------------------------------

    def keys(self):

        return sorted(self._cache.keys())


chat_cache_service = ChatCacheService()