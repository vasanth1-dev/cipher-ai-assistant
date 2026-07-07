import threading
import time

from core.listener import listener
from core.speaker import speaker
from core.router import router
from core.wakeword import wakeword
from core.logger import logger
from core.reminder_worker import reminder_worker

from services.history_service import history_service
from services.ai_service import ai_service

from config import (
    ASSISTANT_NAME,
    USER_NAME,
    SESSION_TIMEOUT,
    EXIT_COMMANDS,
)


class Cipher:

    def __init__(self):

        self.active = False
        self.running = True
        self.processing = False

        self.last_activity = time.time()

        #GUI callbacks
        self.on_message = None
        self.on_status = None

    # -------------------------------------------------- #
    # State
    # -------------------------------------------------- #

    def activate(self):

        self.active = True
        self.last_activity = time.time()

        if self.on_status:
            self.on_status("🟢 Active")

        if self.on_message:
            self.on_message(
                "Cipher",
                f"Hello {USER_NAME}. I am {ASSISTANT_NAME}. How can I help you?"
            )

        speaker.speak(
            f"Hello {USER_NAME}. I am {ASSISTANT_NAME}. How can I help you?"
        )

    def sleep(self):

        self.active = False

        if self.on_status:
            self.on_status("😴 Sleeping")

        if self.on_message:
            self.on_message(
                "Cipher",
                "Going to sleep."
            )

        speaker.speak("Going to sleep.")

    def stop(self):

        self.running = False

        try:
            reminder_worker.stop()
        except Exception as e:
            logger.exception(e)

    # -------------------------------------------------- #
    # Processing
    # -------------------------------------------------- #

    def process(self, command):

        if self.processing:
            return

        if not command:
            return

        command = command.strip()

        if not command:
            return
        

        if self.on_status:
            self.on_status("🧠 Thinking...")

        self.processing = True

        self.last_activity = time.time()

        print(f"\nYou : {command}")

        logger.info(f"USER : {command}")

        try:

            response = router.route(command)

            if response is not None:

                if self.on_message:
                    self.on_message(
                        "Cipher",
                        response,
                    )

                history_service.add(command, response)

                logger.info(f"CIPHER : {response}")

                speaker.speak(response)

                return

            full_response = ""

            for sentence in ai_service.stream(command):

                if not sentence:
                    continue

                sentence = sentence.strip()

                if not sentence:
                    continue

                full_response += sentence + " "

                logger.info(f"CIPHER : {sentence}")

                if self.on_message:
                    self.on_message(
                        "Cipher",
                        sentence,
                    )

                speaker.speak(sentence)

            full_response = full_response.strip()

            if full_response:

                history_service.add(
                    command,
                    full_response,
                )

        except Exception as e:

            logger.exception(e)

            print(e)

            if self.on_message:
                self.on_message(
                    "Cipher",
                    "Sorry. Something went wrong"
                )

            speaker.speak(
                "Sorry. Something went wrong."
            )

        finally:

            self.processing = False

            if self.on_status:
                self.on_status("🟢 Ready")

    # -------------------------------------------------- #
    # Main Loop
    # -------------------------------------------------- #

    def run(self):

        try:
            reminder_worker.start()
        except Exception as e:
            logger.exception(e)

        if self.on_status:
            self.on_status("🟢 Online")

        if self.on_message:
            self.on_message(
                "System",
                f"{ASSISTANT_NAME} is online"
            )

        speaker.speak(
            f"{ASSISTANT_NAME} is online."
        )

        while self.running:

            try:

                if self.active:

                    if (
                        time.time() - self.last_activity
                        > SESSION_TIMEOUT
                    ):

                        self.sleep()

                        continue

                text = listener.listen()

                if not text:
                    continue

                text = text.lower().strip()

                # ---------------- Wake Mode ---------------- #

                if not self.active:

                    if wakeword.detect(text):

                        self.activate()

                        command = wakeword.remove(text)

                        if command:

                            threading.Thread(
                                target=self.process,
                                args=(command,),
                                daemon=True,
                            ).start()

                    continue

                # ---------------- Exit ---------------- #

                if text in EXIT_COMMANDS:

                    speaker.speak("Goodbye.")

                    self.stop()

                    break

                # ---------------- Sleep ---------------- #

                if text in (
                    "sleep",
                    "go to sleep",
                    "stop listening",
                ):

                    self.sleep()

                    continue

                threading.Thread(
                    target=self.process,
                    args=(text,),
                    daemon=True,
                ).start()

            except KeyboardInterrupt:

                self.stop()

                break

            except Exception as e:

                logger.exception(e)

                time.sleep(1)