from services.notification_service import notification_service

INTENT = "notification"


def handle(command: str):

    if not command:
        return None

    command = command.lower().strip()

    if command.startswith("notify"):

        message = command.replace("notify", "", 1).strip()

        if not message:
            return "What should I notify?"

        success = notification_service.notify(
            "Cipher",
            message,
        )

        if success:
            return "Notification sent."

        return "Unable to send the notification."

    return None