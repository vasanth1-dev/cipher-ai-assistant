from services.reminder_service import reminder_service
from services.time_parser import time_parser


def handle(command: str):

    command = command.lower().strip()

    # ---------------------------------
    # Show reminders
    # ---------------------------------

    if command in (
        "show reminders",
        "list reminders",
        "my reminders",
    ):
        return reminder_service.list()

    # ---------------------------------
    # Complete reminder
    # ---------------------------------

    if command.startswith("complete reminder"):

        try:
            number = int(command.split()[-1])
            return reminder_service.complete(number)
        except Exception:
            return "Please specify a valid reminder number."

    # ---------------------------------
    # Delete reminder
    # ---------------------------------

    if command.startswith("delete reminder"):

        try:
            number = int(command.split()[-1])
            return reminder_service.delete(number)
        except Exception:
            return "Please specify a valid reminder number."

    # ---------------------------------
    # Clear completed reminders
    # ---------------------------------

    if command in (
        "clear reminders",
        "clear completed reminders",
    ):
        return reminder_service.clear_completed()

    # ---------------------------------
    # Add reminder
    # ---------------------------------

    if command.startswith("remind me to "):

        text = command.replace("remind me to ", "", 1)

        separators = (
            " at ",
            " in ",
            " tomorrow ",
            " today ",
        )

        reminder_text = None
        time_text = None

        for sep in separators:

            if sep in text:

                left, right = text.split(sep, 1)

                reminder_text = left.strip()

                if sep.strip() == "in":
                    time_text = f"in {right.strip()}"
                elif sep.strip() == "at":
                    time_text = right.strip()
                else:
                    time_text = f"{sep.strip()} {right.strip()}"

                break

        if not reminder_text or not time_text:
            return (
                "Example: remind me to call mom in 30 minutes."
            )

        remind_at = time_parser.parse(time_text)

        if not remind_at:
            return "I couldn't understand the reminder time."

        return reminder_service.add(
            reminder_text,
            remind_at,
        )

    return None