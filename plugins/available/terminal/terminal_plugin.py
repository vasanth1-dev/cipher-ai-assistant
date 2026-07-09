from __future__ import annotations

from plugins.base_plugin import BasePlugin
from plugins.plugin_manifest import PluginManifest
from services.terminal_service import terminal_service


class TerminalPlugin(BasePlugin):
    """
    Built-in Terminal plugin.

    Delegates terminal operations to Cipher's
    TerminalService.
    """

    def __init__(self):

        super().__init__()

        self.manifest = PluginManifest(
            name="terminal",
            version="1.0.0",
            author="Cipher",
            description="Execute terminal operations through the Terminal Service.",
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
            "terminal ",
            "run command ",
            "execute ",
            "execute command ",
            "shell ",
            "bash ",
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

            if lower.startswith("terminal "):

                cmd = command[len("terminal "):].strip()

                return terminal_service.execute(cmd)

            if lower.startswith("run command "):

                cmd = command[len("run command "):].strip()

                return terminal_service.execute(cmd)

            if lower.startswith("execute command "):

                cmd = command[len("execute command "):].strip()

                return terminal_service.execute(cmd)

            if lower.startswith("execute "):

                cmd = command[len("execute "):].strip()

                return terminal_service.execute(cmd)

            if lower.startswith("shell "):

                cmd = command[len("shell "):].strip()

                return terminal_service.execute(cmd)

            if lower.startswith("bash "):

                cmd = command[len("bash "):].strip()

                return terminal_service.execute(cmd)

            return "Unsupported terminal command."

        except Exception as e:

            return f"Terminal error: {e}"