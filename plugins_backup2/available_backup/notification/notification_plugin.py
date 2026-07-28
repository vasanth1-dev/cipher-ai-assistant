from __future__ import annotations

from plugins.base_plugin import Plugin
from plugins.plugin_manifest import PluginManifest
from services.notification_service import notification_service


class NotificationPlugin(BasePlugin):
    """
    Built-in Notification plugin.

    Delegates desktop notification operations to
    Cipher's NotificationService.
    """

    def __init__(
       self,
    ) -> None:

        super().__init__()

        self.manifest = PluginManifest(
            name="notification",
            version="1.0.0",
            author="Cipher",
            description="Display and manage desktop notifications.",
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
            "notify ",
            "show notification ",
            "notification ",
            "clear notifications",
            "dismiss notifications",
            "notification history",
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

            if lower.startswith("notify "):

                message = command[len("notify "):].strip()

                if not message:
                    return "Please provide a notification message."

                return notification_service.notify(message)

            if lower.startswith("show notification "):

                message = command[
                    len("show notification "):
                ].strip()

                if not message:
                    return "Please provide a notification message."

                return notification_service.notify(message)

            if lower.startswith("notification "):

                message = command[
                    len("notification "):
                ].strip()

                if not message:
                    return "Please provide a notification message."

                return notification_service.notify(message)

            if lower == "clear notifications":
                return notification_service.clear()

            if lower == "dismiss notifications":
                return notification_service.dismiss_all()

            if lower == "notification history":
                return notification_service.history()

            return "Unsupported notification command."

        except Exception as e:

            return f"Notification error: {e}"