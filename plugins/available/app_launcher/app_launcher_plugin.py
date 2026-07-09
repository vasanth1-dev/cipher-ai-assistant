from __future__ import annotations

from plugins.base_plugin import BasePlugin
from plugins.plugin_manifest import PluginManifest
from services.app_launcher_service import app_launcher_service


class AppLauncherPlugin(BasePlugin):
    """
    Built-in Application Launcher plugin.

    Delegates application launching to Cipher's
    AppLauncherService.
    """

    def __init__(self):

        super().__init__()

        self.manifest = PluginManifest(
            name="app_launcher",
            version="1.0.0",
            author="Cipher",
            description="Launch, close and manage desktop applications.",
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
            "open application ",
            "open app ",
            "launch ",
            "start ",
            "run ",
            "close ",
            "quit ",
            "kill ",
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

            if lower.startswith("open application "):

                app = command[len("open application "):].strip()

                return app_launcher_service.launch(app)

            if lower.startswith("open app "):

                app = command[len("open app "):].strip()

                return app_launcher_service.launch(app)

            if lower.startswith("launch "):

                app = command[len("launch "):].strip()

                return app_launcher_service.launch(app)

            if lower.startswith("start "):

                app = command[len("start "):].strip()

                return app_launcher_service.launch(app)

            if lower.startswith("run "):

                app = command[len("run "):].strip()

                return app_launcher_service.launch(app)

            if lower.startswith("close "):

                app = command[len("close "):].strip()

                return app_launcher_service.close(app)

            if lower.startswith("quit "):

                app = command[len("quit "):].strip()

                return app_launcher_service.close(app)

            if lower.startswith("kill "):

                app = command[len("kill "):].strip()

                return app_launcher_service.kill(app)

            return "Unsupported application command."

        except Exception as e:

            return f"Application launcher error: {e}"