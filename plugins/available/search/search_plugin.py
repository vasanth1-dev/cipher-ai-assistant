from __future__ import annotations

from plugins.base_plugin import BasePlugin
from plugins.plugin_manifest import PluginManifest
from services.search_service import search_service


class SearchPlugin(BasePlugin):
    """
    Built-in Search plugin.

    Delegates all search operations to Cipher's SearchService.
    """

    def __init__(self):

        super().__init__()

        self.manifest = PluginManifest(
            name="search",
            version="1.0.0",
            author="Cipher",
            description="Search the web and local resources.",
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
            "search ",
            "search for ",
            "find ",
            "look up ",
            "lookup ",
            "google ",
        )

        return command.startswith(prefixes)

    # --------------------------------------------------
    # Command Handler
    # --------------------------------------------------

    def handle(
        self,
        command: str,
    ) -> str:

        query = self._extract_query(command)

        if not query:
            return "Please tell me what you want to search for."

        try:

            return search_service.search(query)

        except Exception as e:

            return f"Search failed: {e}"

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    @staticmethod
    def _extract_query(
        command: str,
    ) -> str:

        lower = command.lower()

        prefixes = (
            "search for ",
            "search ",
            "look up ",
            "lookup ",
            "find ",
            "google ",
        )

        for prefix in prefixes:

            if lower.startswith(prefix):

                return command[len(prefix):].strip()

        return ""