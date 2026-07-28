from __future__ import annotations

from plugins.base_plugin import BasePlugin
from plugins.plugin_manifest import PluginManifest
from services.system_service import system_service


class SystemPlugin(BasePlugin):
    """
    Built-in System plugin.

    Delegates operating system actions to Cipher's
    SystemService.
    """

    def __init__(
       self,
    ) -> None:

        super().__init__()

        self.manifest = PluginManifest(
            id=self.name.lower().replace(" ", "_"),
            name="system",
            version="1.0.0",
            author="Cipher",
            description="Provides operating system control.",
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
            "shutdown",
            "restart",
            "reboot",
            "lock screen",
            "logout",
            "sign out",
            "sleep",
            "hibernate",
            "mute",
            "unmute",
            "volume",
            "brightness",
            "take screenshot",
            "screenshot",
        )

        return command.startswith(prefixes)

    # --------------------------------------------------
    # Command Handler
    # --------------------------------------------------

    def handle(
        self,
        command: str,
    ) -> str:

        command = command.strip().lower()

        try:

            if command == "shutdown":
                return system_service.shutdown()

            if command in ("restart", "reboot"):
                return system_service.restart()

            if command == "lock screen":
                return system_service.lock_screen()

            if command in ("logout", "sign out"):
                return system_service.logout()

            if command == "sleep":
                return system_service.sleep()

            if command == "hibernate":
                return system_service.hibernate()

            if command == "mute":
                return system_service.mute()

            if command == "unmute":
                return system_service.unmute()

            if command.startswith("volume"):
                return system_service.set_volume(command)

            if command.startswith("brightness"):
                return system_service.set_brightness(command)

            if command in (
                "take screenshot",
                "screenshot",
            ):
                return system_service.take_screenshot()

            return "Unsupported system command."

        except Exception as e:

            return f"System command failed: {e}"