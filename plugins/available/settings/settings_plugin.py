from __future__ import annotations

from plugins.base_plugin import BasePlugin
from plugins.plugin_manifest import PluginManifest
from services.settings_service import settings_service


class SettingsPlugin(BasePlugin):
    """
    Built-in Settings plugin.

    Delegates all settings operations to Cipher's
    SettingsService.
    """

    def __init__(self):

        super().__init__()

        self.manifest = PluginManifest(
            name="settings",
            version="1.0.0",
            author="Cipher",
            description="Manage Cipher settings and preferences.",
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
            "settings",
            "show settings",
            "open settings",
            "reload settings",
            "reset settings",
            "set ",
            "change ",
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

            if lower == "settings":
                return settings_service.summary()

            if lower == "show settings":
                return settings_service.summary()

            if lower == "open settings":
                return settings_service.open()

            if lower == "reload settings":
                settings_service.reload()
                return "Settings reloaded."

            if lower == "reset settings":
                settings_service.reset()
                return "Settings reset successfully."

            if lower.startswith("set "):

                request = command[4:].strip()

                return settings_service.set(request)

            if lower.startswith("change "):

                request = command[7:].strip()

                return settings_service.change(request)

            return "Unsupported settings command."

        except Exception as e:

            return f"Settings error: {e}"