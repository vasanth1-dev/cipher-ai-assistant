from __future__ import annotations

from pathlib import Path


class ChatClipboardService:
    """
    Stores a local clipboard history for Cipher.

    This service is independent from the system clipboard.
    It is intended for conversation snippets, prompts,
    and code blocks copied inside Cipher.
    """

    MAX_HISTORY = 100

    def __init__(self):

        self._history: list[str] = []

    # --------------------------------------------------

    def copy(
        self,
        text: str,
    ):

        text = text.strip()

        if not text:
            return

        if text in self._history:
            self._history.remove(text)

        self._history.insert(0, text)

        self._history = self._history[: self.MAX_HISTORY]

    # --------------------------------------------------

    def latest(self) -> str:

        if not self._history:
            return ""

        return self._history[0]

    # --------------------------------------------------

    def history(self) -> list[str]:

        return list(self._history)

    # --------------------------------------------------

    def get(
        self,
        index: int,
    ) -> str:

        if 0 <= index < len(self._history):
            return self._history[index]

        return ""

    # --------------------------------------------------

    def remove(
        self,
        index: int,
    ) -> bool:

        if 0 <= index < len(self._history):
            del self._history[index]
            return True

        return False

    # --------------------------------------------------

    def clear(self):

        self._history.clear()

    # --------------------------------------------------

    def count(self) -> int:

        return len(self._history)


chat_clipboard_service = ChatClipboardService()