from __future__ import annotations

from pathlib import Path


class PromptLoader:
    """
    Loads and caches Cipher prompt files.
    """

    def __init__(self):

        self.folder = Path("prompts")

        self._cache = {}

    # --------------------------------------------------

    def load(
        self,
        name: str,
    ) -> str:

        if name in self._cache:
            return self._cache[name]

        file = self.folder / f"{name}.txt"

        if not file.exists():

            self._cache[name] = ""

            return ""

        text = file.read_text(
            encoding="utf-8",
        ).strip()

        self._cache[name] = text

        return text

    # --------------------------------------------------

    def reload(self):

        self._cache.clear()

    # --------------------------------------------------

    def exists(
        self,
        name: str,
    ) -> bool:

        return (
            self.folder / f"{name}.txt"
        ).exists()

    # --------------------------------------------------

    def available(self):

        return sorted(
            file.stem
            for file in self.folder.glob("*.txt")
        )


prompt_loader = PromptLoader()