from __future__ import annotations

from pathlib import Path
from core.logger import logger


class PromptLoader:
    """
    Loads and caches Cipher prompt files.
    """

    def __init__(
       self,
    ) -> None:

        self.folder = Path("prompts")

        self._cache = {}

    # --------------------------------------------------

    def load(
        self,
        name: str,
    ) -> str:

        if name in self._cache:
            return self._cache[name]

        prompt_file = self._prompt_path(
            name,
        )

        if not prompt_file.exists():

            self._cache[name] = ""

            return ""
        

        try:
            text = prompt_file.read_text(
                encoding="utf-8",
            ).strip()

        except Exception as e:

            logger.exception(
                f"[PROMPT] Failed to load '{name}': {e}"
            )

            text = ""

        self._cache[name] = text

        return text
    
    def _prompt_path(
        self,
        name: str,
    ) -> Path:
        return self.folder / f"{name}.txt"

    # --------------------------------------------------

    def reload(
        self,
    ) -> None:

        self._cache.clear()

        logger.info(
            "[PROMPT] Cache cleared."
        )

    # --------------------------------------------------

    def exists(
        self,
        name: str,
    ) -> bool:

        return self._prompt_path(
            name,
        ).exists()

    # --------------------------------------------------

    def available(
        self
    ) -> list[str]:

        return sorted(
            file.stem
            for file in self.folder.glob("*.txt")
        )


prompt_loader = PromptLoader()