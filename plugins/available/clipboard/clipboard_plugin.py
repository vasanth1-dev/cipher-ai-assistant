from __future__ import annotations

from plugins.base_plugin import BasePlugin
from plugins.plugin_manifest import PluginManifest
from services.clipboard_service import clipboard_service


class ClipboardPlugin(BasePlugin):
    """
    Built-in Clipboard plugin.

    Delegates clipboard operations to Cipher's
    ClipboardService.
    """

    def __init__(self):

        super().__init__()

        self.manifest = PluginManifest(
            name="clipboard",
            version="1.0.0",
            author="Cipher",
            description="Provides clipboard management.",
        )

    # --------------------------------------------------
    # Lifecycle
    # --------------------------------------------------

    def on_load(self) -> None:
        pass

    def on_unload(self) -> None:
        pass

    # --------------------------------------------------
    # Command Detection
    # --------------------------------------------------

    def can_handle(
        self,
        command: str,
    ) -> bool:

        command = command.lower().strip()

        prefixes = (
            "copy ",
            "paste",
            "clipboard",
            "clear clipboard",
            "clipboard history",
        )

        return command.startswith(prefixes)

    # --------------------------------------------------
    # Command Handler
    # --------------------------------------------------

    def handle(
        self,
        command: str,
    ) -> str:

        command = command.strip()

        lower = command.lower()

        try:

            if lower.startswith("copy "):

                text = command[5:].strip()

                if not text:
                    return "Nothing to copy."

                clipboard_service.copy(text)

                return "Copied to clipboard."

            if lower == "paste":

                text = clipboard_service.paste()

                return text if text else "Clipboard is empty."

            if lower == "clipboard":

                text = clipboard_service.paste()

                return text if text else "Clipboard is empty."

            if lower == "clear clipboard":

                clipboard_service.clear()

                return "Clipboard cleared."

            if lower == "clipboard history":

                history = clipboard_service.history()

                if not history:
                    return "Clipboard history is empty."

                return "\n".join(
                    f"{index + 1}. {item}"
                    for index, item in enumerate(history)
                )

            return "Unsupported clipboard command."

        except Exception as e:

            return f"Clipboard error: {e}"