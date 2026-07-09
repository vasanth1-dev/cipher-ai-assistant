from __future__ import annotations

from plugins.base_plugin import BasePlugin
from plugins.plugin_manifest import PluginManifest
from services.network_service import network_service


class NetworkPlugin(BasePlugin):
    """
    Built-in Network plugin.

    Delegates all networking operations to Cipher's
    NetworkService.
    """

    def __init__(self):

        super().__init__()

        self.manifest = PluginManifest(
            name="network",
            version="1.0.0",
            author="Cipher",
            description="Manage network connections and information.",
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
            "wifi",
            "wi-fi",
            "network",
            "connect wifi",
            "disconnect wifi",
            "enable wifi",
            "disable wifi",
            "scan wifi",
            "network status",
            "ip address",
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

            if lower in ("network", "network status"):
                return network_service.status()

            if lower in ("wifi", "wi-fi"):
                return network_service.status()

            if lower == "scan wifi":
                return network_service.scan()

            if lower == "enable wifi":
                return network_service.enable_wifi()

            if lower == "disable wifi":
                return network_service.disable_wifi()

            if lower.startswith("connect wifi"):

                ssid = command[len("connect wifi"):].strip()

                return network_service.connect(ssid)

            if lower == "disconnect wifi":
                return network_service.disconnect()

            if lower == "ip address":
                return network_service.ip_address()

            return "Unsupported network command."

        except Exception as e:

            return f"Network error: {e}"