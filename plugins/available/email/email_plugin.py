from __future__ import annotations

from plugins.base_plugin import BasePlugin
from plugins.plugin_manifest import PluginManifest
from services.email_service import email_service


class EmailPlugin(BasePlugin):
    """
    Built-in Email plugin.

    Delegates email operations to Cipher's EmailService.
    """

    def __init__(self):

        super().__init__()

        self.manifest = PluginManifest(
            name="email",
            version="1.0.0",
            author="Cipher",
            description="Compose, send and manage emails.",
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
            "send email",
            "compose email",
            "draft email",
            "read emails",
            "check email",
            "check inbox",
            "show inbox",
            "email ",
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

            if lower == "read emails":
                return email_service.read()

            if lower == "check email":
                return email_service.check()

            if lower == "check inbox":
                return email_service.check()

            if lower == "show inbox":
                return email_service.inbox()

            if lower.startswith("send email"):

                request = command[len("send email"):].strip()

                return email_service.send(request)

            if lower.startswith("compose email"):

                request = command[len("compose email"):].strip()

                return email_service.compose(request)

            if lower.startswith("draft email"):

                request = command[len("draft email"):].strip()

                return email_service.draft(request)

            if lower.startswith("email "):

                request = command[len("email "):].strip()

                return email_service.send(request)

            return "Unsupported email command."

        except Exception as e:

            return f"Email error: {e}"