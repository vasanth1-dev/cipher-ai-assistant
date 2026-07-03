import time

from config import (
    ASSISTANT_NAME,
    USER_NAME,
    SESSION_TIMEOUT,
)

from core.listener import listener
from core.speaker import speaker
from core.router import router
from core.wakeword import wakeword
from skills.history import save_history

from services.command_parser import parser
from services.command_executor import executor


class Cipher:

    def __init__(self):

        self.active = False
        self.last_activity = time.time()

    def activate(self):

        self.active = True
        self.last_activity = time.time()

        speaker.speak(
            f"Hello {USER_NAME}. How can I help you?"
        )

    def sleep(self):

        self.active = False
        speaker.speak("Going to sleep.")

    def process(self, command):

        if not command:
            return

        self.last_activity = time.time()

        command = parser.parse(command)
        command = executor.normalize(command)

        print(f"\nYou : {command}")
        save_history(command)

        response = router.route(command)

        if response:
            speaker.speak(response)

    def run(self):

        speaker.speak(f"{ASSISTANT_NAME} is online.")

        while True:

            if self.active:

                if time.time() - self.last_activity > SESSION_TIMEOUT:
                    self.sleep()

            text = listener.listen()

            if not text:
                continue

            text = text.lower().strip()

            # ---------- Wake Word ----------

            if not self.active:

                if wakeword.detect(text):

                    self.activate()

                    command = wakeword.remove(text)

                    if command:
                        self.process(command)

                continue

            # ---------- Exit ----------

            if text in (
                "exit",
                "quit",
                "goodbye",
                "stop",
            ):

                speaker.speak("Goodbye.")
                break

            # ---------- Sleep ----------

            if text in (
                "sleep",
                "go to sleep",
                "stop listening",
            ):

                self.sleep()
                continue

            # ---------- Process ----------

            self.process(text)