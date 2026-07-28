from __future__ import annotations

from plugins.base_plugin import BasePlugin
from plugins.plugin_manifest import PluginManifest
from services.bluetooth_service import bluetooth_service


class BluetoothPlugin(BasePlugin):
    """
    Built-in Bluetooth plugin.

    Delegates Bluetooth operations to Cipher's
    BluetoothService.
    """

    def __init__(
       self,
    ) -> None:

        super().__init__()

        self.manifest = PluginManifest(
            id=self.name.lower().replace(" ", "_"),
            name="bluetooth",
            version="1.0.0",
            author="Cipher",
            description="Manage Bluetooth devices and connections.",
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
            "bluetooth",
            "bluetooth status",
            "turn on bluetooth",
            "turn off bluetooth",
            "enable bluetooth",
            "disable bluetooth",
            "scan bluetooth",
            "pair bluetooth",
            "connect bluetooth",
            "disconnect bluetooth",
            "bluetooth devices",
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
                "bluetooth",
                "bluetooth status",
            ):
                return bluetooth_service.status()

            if lower in (
                "turn on bluetooth",
                "enable bluetooth",
            ):
                return bluetooth_service.enable()

            if lower in (
                "turn off bluetooth",
                "disable bluetooth",
            ):
                return bluetooth_service.disable()

            if lower == "scan bluetooth":
                return bluetooth_service.scan()

            if lower == "bluetooth devices":
                return bluetooth_service.devices()

            if lower.startswith("pair bluetooth"):

                device = command[
                    len("pair bluetooth"):
                ].strip()

                return bluetooth_service.pair(device)

            if lower.startswith("connect bluetooth"):

                device = command[
                    len("connect bluetooth"):
                ].strip()

                return bluetooth_service.connect(device)

            if lower.startswith("disconnect bluetooth"):

                device = command[
                    len("disconnect bluetooth"):
                ].strip()

                return bluetooth_service.disconnect(device)

            return "Unsupported Bluetooth command."

        except Exception as e:

            return f"Bluetooth error: {e}"