import subprocess


class NotificationService:

    def notify(
        self,
        title: str,
        message: str,
        icon: str = "dialog-information",
    ):

        try:

            subprocess.run(
                [
                    "notify-send",
                    title,
                    message,
                    "-i",
                    icon,
                ],
                check=False,
            )

            return True

        except Exception:
            return False


notification_service = NotificationService()