from __future__ import annotations

from plugins.base_plugin import Plugin
from plugins.plugin_manifest import PluginManifest
from services.calendar_service import calendar_service


class CalendarPlugin(BasePlugin):
    """
    Built-in Calendar plugin.

    Delegates calendar operations to Cipher's
    CalendarService.
    """

    def __init__(
       self,
    ) -> None:

        super().__init__()

        self.manifest = PluginManifest(
            id=self.name.lower().replace(" ", "_"),
            name="calendar",
            version="1.0.0",
            author="Cipher",
            description="Manage calendar events and schedules.",
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
            "create event",
            "add event",
            "schedule meeting",
            "calendar",
            "show calendar",
            "show events",
            "list events",
            "today events",
            "delete event",
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

            if lower == "calendar":
                return calendar_service.today()

            if lower == "show calendar":
                return calendar_service.show()

            if lower == "show events":
                return calendar_service.list()

            if lower == "list events":
                return calendar_service.list()

            if lower == "today events":
                return calendar_service.today()

            if lower.startswith("create event"):

                request = command[len("create event"):].strip()

                return calendar_service.create(request)

            if lower.startswith("add event"):

                request = command[len("add event"):].strip()

                return calendar_service.create(request)

            if lower.startswith("schedule meeting"):

                request = command[len("schedule meeting"):].strip()

                return calendar_service.schedule_meeting(
                    request
                )

            if lower.startswith("delete event"):

                request = command[len("delete event"):].strip()

                return calendar_service.delete(request)

            return "Unsupported calendar command."

        except Exception as e:

            return f"Calendar error: {e}"