import threading
import time

from core.listener import listener
from core.speaker import speaker
from core.router import router
from core.wakeword import wakeword
from core.logger import logger
from core.reminder_worker import reminder_worker




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
        self.processing_lock = threading.Lock()

        self.last_activity = time.time()

        # GUI callbacks
        self.on_message = None
        self.on_status = None

        # Streaming callbacks
        self.on_stream_start = None
        self.on_stream_update = None
        self.on_stream_finish = None

    # -------------------------------------------------- #
    # State
    # -------------------------------------------------- #

    def activate(self):

        self.active = True
        self.last_activity = time.time()

        if self.on_status:
            self.on_status("🟢 Active")

        message = (
            f"Hello {USER_NAME}. "
            f"I am {ASSISTANT_NAME}. "
            f"How can I help you?"
        )

        speaker.speak(message)

    def sleep(self):

        self.active = False

        if self.on_status:
            self.on_status("😴 Sleeping")

        if self.on_message:
            self.on_message(
                "Cipher",
                "Going to sleep.",
            )

        speaker.speak("Going to sleep.")

    def stop(self):

        self.running = False

        try:
            reminder_worker.stop()
            speaker.stop()

        except Exception as e:
            logger.exception(e)

        try:

            from plugins import plugin_manager

            if plugin_manager.started:
                plugin_manager.stop()

        except Exception as e:

            logger.exception(e)

        try:

            listener.stop()

        except Exception:
            pass
    # -------------------------------------------------- #
    # Processing
    # -------------------------------------------------- #

    def process(self, command):

        

        if not command:
            return

        command = command.strip()

        if not command:
            return
        
        with self.processing_lock:

            if self.processing:
                return

            self.processing = True

        self.last_activity = time.time()

        if self.on_status:
            self.on_status("🧠 Thinking...")

        logger.info(f"USER : {command}")

        try:

            response = router.route(command)

            print("ROUTER RESPONSE =>", repr(response))

            # -----------------------------
            # Local skill response
            # -----------------------------

            if response:

    # Save assistant reply
                try:
                    from core.conversation.conversation_service import conversation_service

                    conversation_service.add_assistant_message(response)

                except Exception as e:
                    logger.exception(e)

                # Update GUI
                if self.on_message:
                    self.on_message(
                        "Cipher",
                        response,
                    )

                logger.info(
                    f"CIPHER : {response}"
                )

                speaker.speak(response)

                return

            

        except Exception as e:

            logger.exception(e)

            if self.on_message:
                self.on_message(
                    "Cipher",
                    "Sorry. Something went wrong."
                )

            speaker.speak(
                "Sorry. Something went wrong."
            )

        finally:
            
            with self.processing_lock:
                self.processing = False

            if self.on_status:
                self.on_status("🟢 Ready")
    
        # -------------------------------------------------- #
    # Single Listen (GUI ST Button)
    # -------------------------------------------------- #

    def listen_once(self):

        if self.processing:
            return

        if self.on_status:
            self.on_status("🎤 Listening...")

        try:

            text = listener.listen()

            print("RAW STT =>", repr(text))

            if not text:

                if self.on_status:
                    self.on_status("🟢 Ready")

                return

            text = text.strip()

            if self.on_message:
                self.on_message(
                    USER_NAME,
                    text,
                )

            self.process(text)

        except Exception as e:

            logger.exception(e)

            if self.on_message:
                self.on_message(
                    "System",
                    f"Speech Error: {e}",
                )

        finally:

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

        try:

            from plugins import plugin_manager

            if not plugin_manager.started:
                plugin_manager.start()

        except Exception as e:
            logger.exception(e)

        if self.on_status:
            self.on_status("🟢 Online")

        if self.on_message:
            self.on_message(
                "System",
                f"{ASSISTANT_NAME} is online",
            )

        speaker.speak(
            f"{ASSISTANT_NAME} is online."
        )

        while self.running:

            try:

                if self.active:

                    if (
                        time.time()
                        - self.last_activity
                        > SESSION_TIMEOUT
                    ):

                        self.sleep()
                        continue

                if self.processing:
                    time.sleep(0.1)
                    continue


                text = listener.listen()

                if not text:
                    continue

                text = text.lower().strip()

                # Wake Mode

                if not self.active:

                    if wakeword.detect(text):

                        command = wakeword.remove(
                            text
                        )

                        if not self.active:
                            self.activate()

                        if command:

                            threading.Thread(
                                target=self.process,
                                args=(text,),
                                daemon=True,
                                name="CipherCommand"
                            ).start()

                    continue

                # Exit

                if text in EXIT_COMMANDS:

                    speaker.speak(
                        "Goodbye."
                    )

                    self.stop()

                    break

                # Sleep

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