import threading
import time

from services.reminder_service import reminder_service
from services.notification_service import notification_service
from core.speaker import speaker


class SchedulerService:

    def __init__(
       self,
    ) -> None:
        self.running = False

    def loop(self):

        while self.running:

            reminders = reminder_service.due()

            for message in reminders:

                notification_service.notify(
                    "Cipher Reminder",
                    message,
                )

                speaker.speak(
                    f"Vasanth, this is your reminder. {message}"
                )

            time.sleep(10)

    def start(self):

        if self.running:
            return

        self.running = True

        self.thread = threading.Thread(
            target=self.loop,
            daemon=True,
            name="SchedulerService"
        )

        self.thread.start()

    def stop(self):
        self.running = False

        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2)
            
        self.thread = None


scheduler_service = SchedulerService()