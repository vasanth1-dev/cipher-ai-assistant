from __future__ import annotations

from plugins.base_plugin import Plugin
from plugins.plugin_manifest import PluginManifest
from services.browser_service import browser_service


class BrowserPlugin(BasePlugin):
    """
    Built-in Browser plugin.

    Delegates browser-related operations to Cipher's
    BrowserService.
    """

    def __init__(
       self,
    ) -> None:

        super().__init__()

        self.manifest = PluginManifest(
            name="browser",
            version="1.0.0",
            author="Cipher",
            description="Open websites and perform browser actions.",
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
            "open ",
            "browse ",
            "go to ",
            "visit ",
            "open website ",
            "open url ",
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

            if lower.startswith("open website "):

                url = command[len("open website "):].strip()

                return browser_service.open(url)

            if lower.startswith("open url "):

                url = command[len("open url "):].strip()

                return browser_service.open(url)

            if lower.startswith("browse "):

                target = command[len("browse "):].strip()

                return browser_service.browse(target)

            if lower.startswith("go to "):

                target = command[len("go to "):].strip()

                return browser_service.open(target)

            if lower.startswith("visit "):

                target = command[len("visit "):].strip()

                return browser_service.open(target)

            if lower.startswith("open "):

                target = command[len("open "):].strip()

                return browser_service.open(target)

            return "Unsupported browser command."

        except Exception as e:

            return f"Browser error: {e}"