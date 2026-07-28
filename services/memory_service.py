import json
from pathlib import Path

from core.logger import logger


class MemoryService:

    def __init__(
       self,
    ) -> None:

        self.file = Path("data/memory.json")

        self.file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not self.file.exists():
            self._save({})

        self._memory = self._load()

    # ------------------------------------------------ #
    # Internal
    # ------------------------------------------------ #

    def _load(self):

        try:

            with open(
                self.file,
                "r",
                encoding="utf-8",
            ) as f:

                data = json.load(f)

                if isinstance(data, dict):
                    return data

        except Exception as e:

            logger.exception(
                f"[MEMORY] Failed to load memory: {e}"
            )

        return {}

    def _save(self, data):

        try:

            with open(
                self.file,
                "w",
                encoding="utf-8",
            ) as f:

                json.dump(
                    data,
                    f,
                    indent=4,
                    ensure_ascii=False,
                    sort_keys=True,
                )

        except Exception as e:

            logger.exception(
                f"[MEMORY] Failed to save memory: {e}"
            )

    def _commit(
        self,
    ) -> None:
        """
        Save the in-memory cache to disk.
        """

        self._save(
            self._memory
        )

    def _normalize_key(
        self,
        key: str,
    ) -> str:
        """
        Normalize memory keys.
        """

        return str(key).strip().lower()

    # ------------------------------------------------ #
    # Public API
    # ------------------------------------------------ #

    def remember(self, key, value):

        if not key or value is None:
            return False

        data = self._memory

        key = self._normalize_key(
            key,
        )

        if not key:
            return False

        data[key] = value

        self._commit()

        logger.info(f"[MEMORY] Saved: {key}")

        return True

    def recall(self, key):

        if not key:
            return None

        data = self._memory

        key = self._normalize_key(
            key,
        )

        return data.get(key)

    def update(self, key, value):

        return self.remember(key, value)

    def forget(self, key):

        if not key:
            return False

        data = self._memory

        key = self._normalize_key(
            key,
        )

        if key not in data:
            return False

        del data[key]

        self._commit()

        logger.info(f"[MEMORY] Removed: {key}")

        return True

    def exists(self, key):

        if not key:
            return False

        key = self._normalize_key(
            key,
        )

        return key in self._memory

    def search(self, keyword):

        if not keyword:
            return {}

        keyword = self._normalize_key(keyword)

        if not keyword:
            return {}

        return {

            k: v

            for k, v in self._memory.items()

            if keyword in k.lower()
            or keyword in str(v).lower()

        }

    def all(self):

        return dict(self._memory)

    def keys(self):

        return sorted(
            self._memory.keys()
        )

    def clear(self):

        self._memory.clear()

        self._commit()

        logger.info("[MEMORY] Cleared.")

    def count(self):

        return len(
            self._memory
        )

    # ------------------------------------------------ #
    # AI Context
    # ------------------------------------------------ #

    def memory_prompt(self):

        data = self._memory

        if not data:
            return ""

        lines = [
            "Known facts about the user:"
        ]

        for key, value in sorted(data.items()):

            lines.append(
                f"- {key}: {value}"
            )

        return "\n".join(lines)


memory_service = MemoryService()