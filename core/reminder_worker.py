import threading
import time

from core.logger import logger
from core.speaker import speaker

from services.reminder_service import reminder_service


class ReminderWorker:

    def __init__(
       self,
    ) -> None:

        self.running = False
        self.thread = None

    def start(
        self,
    ) ->None:

        if self.running:
            return

        self.running = True

        self.thread = threading.Thread(
            target=self._run,
            daemon=True,
            name="ReminderWorker",
        )

        self.thread.start()

        logger.info("Reminder worker started.")

    def stop(
        self,
    ) -> None:

        self.running = False

        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2)

        self.thread = None

        logger.info("Reminder worker stopped.")


    def _run(
        self,
    ) -> None:

        while self.running:

            try:

                due = reminder_service.due()

                for reminder in due:

                    logger.info(f"Reminder Due : {reminder}")

                    try:
                        speaker.speak(f"Reminder. {reminder}")
                    except Exception:
                        logger.exception(
                            "Failed to announce reminder."
                        )

            except Exception:

                logger.exception(
                    "Reminder worker loop failed."
                )

            time.sleep(5)


reminder_worker = ReminderWorker()