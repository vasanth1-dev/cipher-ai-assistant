from datetime import datetime

from services.calendar_service import calendar_service
from services.time_parser import time_parser


def handle(command: str):

    command = command.lower().strip()

    # -----------------------------
    # Show Calendar
    # -----------------------------

    if command in (
        "show calendar",
        "calendar",
        "my calendar",
        "list events",
    ):
        return calendar_service.list()

    # -----------------------------
    # Delete Event
    # -----------------------------

    if command.startswith("delete event"):

        try:

            number = int(
                command.replace(
                    "delete event",
                    "",
                    1,
                ).strip()
            )

            return calendar_service.delete(number)

        except Exception:

            return "Please tell the event number."

    # -----------------------------
    # Add Event
    # -----------------------------

    if command.startswith("add event"):

        parsed = time_parser.parse(command)

        title = command.replace(
            "add event",
            "",
            1,
        ).strip()

        if parsed:
            event_time = parsed.isoformat()
        else:
            event_time = datetime.now().isoformat()

        return calendar_service.add(
            title,
            event_time,
        )

    return None