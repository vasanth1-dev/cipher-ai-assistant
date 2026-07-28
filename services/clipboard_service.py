from __future__ import annotations

import pyperclip


class ClipboardService:
    """
    Clipboard Service.

    Provides basic clipboard operations.
    """

    def copy(self, text: str) -> str:
        pyperclip.copy(text)
        return "Text copied to clipboard."

    def paste(self) -> str:
        return pyperclip.paste()

    def clear(self) -> str:
        pyperclip.copy("")
        return "Clipboard cleared."

    def execute(self, command: str) -> str:
        command = command.strip()

        if not command:
            return "Please provide a clipboard command."

        return f"Clipboard service received: {command}"


clipboard_service = ClipboardService()