import time

from core.listener import listener
from core.speaker import speaker
from core.router import router
from core.wakeword import wakeword
from core.error_handler import error_handler
from core.logger import logger

from services.history_service import history_service

from config import (
    ASSISTANT_NAME,
    USER_NAME,
    SESSION_TIMEOUT,
)


class Cipher:

    def __init__(self):
        self.active = False
        self.last_activity = time.time()

    def activate(self):
        self.active = True
        self.last_activity = time.time()

        speaker.speak(
            f"Hello {USER_NAME}. I am {ASSISTANT_NAME}. How can I help you?"
        )

    def sleep(self):
        self.active = False
        speaker.speak("Going to sleep.")

    def process(self, command):

        if not command:
            return

        self.last_activity = time.time()

        print(f"\nYou : {command}")

        logger.info(f"USER : {command}")

        try:
            response = router.route(command)

        except Exception as e:

            response = error_handler.handle(
                e,
                context="Router",
            )

        history_service.add(command, response)

        logger.info(f"CIPHER : {response}")

        if response:
            speaker.speak(response)

    def run(self):

        speaker.speak(f"{ASSISTANT_NAME} is online.")

        while True:

            if self.active:

                if time.time() - self.last_activity > SESSION_TIMEOUT:
                    self.sleep()
                    continue

            text = listener.listen()

            if not text:
                continue

            text = text.lower().strip()

            # Wake mode
            if not self.active:

                if wakeword.detect(text):

                    self.activate()

                    command = wakeword.remove(text)

                    if command:
                        self.process(command)

                continue

            # Exit
            if text in (
                "exit",
                "quit",
                "goodbye",
                "stop",
            ):
                speaker.speak("Goodbye.")
                break

            # Sleep
            if text in (
                "sleep",
                "go to sleep",
                "stop listening",
            ):
                self.sleep()
                continue

            self.process(text)