from datetime import datetime
import re

from services.calendar_service import calendar_service
from services.time_parser import time_parser


def handle(command: str):

    command = " ".join(
        command.lower().strip().split()
    )
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

        patterns = (
            r"\bin\s+\d+\s+(minute|minutes|hour|hours|day|days)\b",
            r"\btomorrow\s+\d{1,2}:\d{2}\b",
            r"\btoday\s+\d{1,2}:\d{2}\b",
            r"\b\d{1,2}:\d{2}\b",
        )

        for pattern in patterns:
            title = re.sub(pattern, "", title).strip()

        title = " ".join(title.split())

        if parsed:
            event_time = parsed
        else:
            event_time = datetime.now().isoformat()

        if not title:
            return "Please provide an event title."

        return calendar_service.add(
            title,
            event_time,
        )

    return None