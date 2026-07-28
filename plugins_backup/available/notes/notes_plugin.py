from __future__ import annotations

from plugins.base_plugin import Plugin
from plugins.plugin_manifest import PluginManifest
from services.notes_service import notes_service


class NotesPlugin(BasePlugin):
    """
    Built-in Notes plugin.

    Delegates all note management to Cipher's NotesService.
    """

    def __init__(
       self,
    ) -> None:

        super().__init__()

        self.manifest = PluginManifest(
            id=self.name.lower().replace(" ", "_"),
            name="notes",
            version="1.0.0",
            author="Cipher",
            description="Create and manage notes.",
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
            "take note",
            "create note",
            "add note",
            "show notes",
            "list notes",
            "my notes",
            "delete note",
            "open note",
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

            if lower in (
                "show notes",
                "list notes",
                "my notes",
            ):
                return notes_service.list()

            if lower.startswith("delete note"):

                title = self._suffix(
                    command,
                    "delete note",
                )

                return notes_service.delete(title)

            if lower.startswith("open note"):

                title = self._suffix(
                    command,
                    "open note",
                )

                return notes_service.open(title)

            if lower.startswith("take note"):

                text = self._suffix(
                    command,
                    "take note",
                )

                return notes_service.add(text)

            if lower.startswith("create note"):

                text = self._suffix(
                    command,
                    "create note",
                )

                return notes_service.add(text)

            if lower.startswith("add note"):

                text = self._suffix(
                    command,
                    "add note",
                )

                return notes_service.add(text)

            return "Unsupported notes command."

        except Exception as e:

            return f"Notes error: {e}"

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    @staticmethod
    def _suffix(
        command: str,
        prefix: str,
    ) -> str:

        return command[len(prefix):].strip()