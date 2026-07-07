from services.notification_service import notification_service


def handle(command: str):

    command = command.lower().strip()

    if command.startswith("notify"):

        message = command.replace("notify", "", 1).strip()

        if not message:
            return "What should I notify?"

        notification_service.notify(
            "Cipher",
            message,
        )

        return "Notification sent."

    return None