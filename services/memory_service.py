import json
from pathlib import Path

from core.logger import logger


class MemoryService:

    def __init__(self):

        self.file = Path("data/memory.json")

        self.file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not self.file.exists():
            self._save({})

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

            logger.exception(e)

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

            logger.exception(e)

    # ------------------------------------------------ #
    # Public API
    # ------------------------------------------------ #

    def remember(self, key, value):

        if not key or value is None:
            return False

        data = self._load()

        key = key.strip().lower()

        data[key] = str(value).strip()

        self._save(data)

        logger.info(f"[MEMORY] Saved: {key}")

        return True

    def recall(self, key):

        if not key:
            return None

        data = self._load()

        return data.get(
            key.strip().lower()
        )

    def update(self, key, value):

        return self.remember(key, value)

    def forget(self, key):

        if not key:
            return False

        data = self._load()

        key = key.strip().lower()

        if key not in data:
            return False

        del data[key]

        self._save(data)

        logger.info(f"[MEMORY] Removed: {key}")

        return True

    def exists(self, key):

        if not key:
            return False

        return (
            key.strip().lower()
            in self._load()
        )

    def search(self, keyword):

        if not keyword:
            return {}

        keyword = keyword.lower()

        return {

            k: v

            for k, v in self._load().items()

            if keyword in k.lower()
            or keyword in str(v).lower()

        }

    def all(self):

        return self._load()

    def keys(self):

        return sorted(
            self._load().keys()
        )

    def clear(self):

        self._save({})

        logger.info("[MEMORY] Cleared.")

    def count(self):

        return len(self._load())

    # ------------------------------------------------ #
    # AI Context
    # ------------------------------------------------ #

    def memory_prompt(self):

        data = self._load()

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