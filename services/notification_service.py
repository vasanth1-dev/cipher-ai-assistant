import shutil
import subprocess

from core.logger import logger


class NotificationService:

    def __init__(self):

        self.command = shutil.which("notify-send")

    # --------------------------------------------------
    # Send Notification
    # --------------------------------------------------

    def notify(
        self,
        title: str,
        message: str,
        icon: str = "dialog-information",
    ):

        title = str(title).strip()
        message = str(message).strip()

        if not title:
            title = "Cipher"

        if not message:
            return False

        if self.command is None:

            logger.warning(
                "[NOTIFICATION] notify-send is not installed."
            )

            return False

        try:

            subprocess.run(
                [
                    self.command,
                    title,
                    message,
                    "-i",
                    icon,
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )

            logger.info(
                f"[NOTIFICATION] {title}: {message}"
            )

            return True

        except Exception as e:

            logger.exception(e)

            return False


notification_service = NotificationService()