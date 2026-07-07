import threading
import time

from services.reminder_service import reminder_service
from services.notification_service import notification_service
from core.speaker import speaker


class SchedulerService:

    def __init__(self):
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

        thread = threading.Thread(
            target=self.loop,
            daemon=True,
        )

        thread.start()

    def stop(self):
        self.running = False


scheduler_service = SchedulerService()