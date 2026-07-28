from __future__ import annotations

import json
from pathlib import Path


class ConversationMemoryService:
    """
    Stores lightweight long-term memory extracted
    from conversations.

    This service is intentionally generic. It does not
    decide what should be remembered; it only stores
    and retrieves memory items.
    """

    def __init__(
       self,
    ) -> None:

        self._file = Path("data/conversation_memory.json")
        self._file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._memory = self._load()

    # --------------------------------------------------

    def _load(self):

        if not self._file.exists():
            return {}

        try:

            with open(
                self._file,
                "r",
                encoding="utf-8",
            ) as file:

                return json.load(file)

        except Exception:
            return {}

    # --------------------------------------------------

    def _save(self):

        with open(
            self._file,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                self._memory,
                file,
                indent=4,
                ensure_ascii=False,
                sort_keys=True,
            )

    # --------------------------------------------------

    def set(
        self,
        key: str,
        value: str,
    ):

        self._memory[key] = value
        self._save()

    # --------------------------------------------------

    def get(
        self,
        key: str,
        default=None,
    ):

        return self._memory.get(
            key,
            default,
        )

    # --------------------------------------------------

    def remove(
        self,
        key: str,
    ):

        if key in self._memory:
            del self._memory[key]
            self._save()

    # --------------------------------------------------

    def exists(
        self,
        key: str,
    ) -> bool:

        return key in self._memory

    # --------------------------------------------------

    def keys(self):

        return sorted(
            self._memory.keys()
        )

    # --------------------------------------------------

    def items(self):

        return dict(self._memory)

    # --------------------------------------------------

    def clear(self):

        self._memory.clear()
        self._save()


conversation_memory_service = ConversationMemoryService()