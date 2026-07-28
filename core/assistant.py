import threading
import time

from core.listener import listener
from core.speaker import speaker
from core.router import router
from core.wakeword import wakeword
from core.logger import logger
from core.reminder_worker import reminder_worker




from config import (
    USER_NAME,
    SESSION_TIMEOUT,
    EXIT_COMMANDS,
)


class Cipher:

    def __init__(
       self,
    ) -> None:

        self.active = False
        self.running = True
        self.processing = False
        self.processing_lock = threading.Lock()
        self.state_lock = threading.Lock()

        self.last_activity = time.time()

        # GUI callbacks
        self.on_message = None
        self.on_status = None

        # Streaming callbacks
        self.on_stream_start = None
        self.on_stream_update = None
        self.on_stream_finish = None
        


    def _set_status(
        self, 
        text: str,
    ) -> None:

        if self.on_status:
            self.on_status(text)

    def _show_message(
        self,
        sender: str,
        message: str,
    ):

        if not message:
            return

        if self.on_message:
            self.on_message(
                sender,
                message.strip(),
            )

    def _speak_response(
        self,
        text: str,
    ):

        if not text:
            return

        speaker.speak(text)


    def _handle_local_response(
        self,
        response: str,
    ):

        response = response.strip()

        if not response:

            if self.on_stream_finish:
                self.on_stream_finish()

            return

        try:
            from core.conversation.conversation_service import (
                conversation_service,
            )

            conversation_service.add_assistant_message(
                response
            )

        except Exception:
            logger.exception("Failed to save assistant message.")


        self._show_message(
            "Cipher",
            response,
        )

        logger.info(
            f"CIPHER : {response}"
        )

       # self._speak_response(
        #    response
       # )
       
        if self.on_stream_finish:
            self.on_stream_finish()

    # -------------------------------------------------- #
    # State
    # -------------------------------------------------- #

    def activate(
        self,
    ) -> None:

        if self.active:
            return

        with self.state_lock:
            self.active = True


        self.last_activity = time.time()

        self._set_status("🟢 Active")
            
        """
        message = (
            f"Hello {USER_NAME}. "
            f"I am {ASSISTANT_NAME}. "
            f"How can I help you?"
        )
        

        speaker.speak(message)
        """

    def sleep(
        self,
    ) -> None:

        with self.state_lock:
            self.active = False

        self._set_status(
            "😴 Sleeping"
        )

    
        self._show_message(
            "Cipher",
            "Going to sleep.",
        )

        self._speak_response("Going to sleep.")

    def stop(
        self,
    ) -> None:

        if not self.running:
            return

        self.running = False

        try:
            reminder_worker.stop()
            speaker.stop()

        except Exception:
            logger.exception("Reminder worker shutdown failed.")

        try:

            from plugins import plugin_manager

            if plugin_manager.started:
                plugin_manager.stop()

        except Exception:
            logger.exception("Reminder worker shutdown failed.")

        try:

            listener.stop()

        except Exception:
            logger.exception("Listener shutdown failed.")
    # -------------------------------------------------- #
    # Processing
    # -------------------------------------------------- #

    def process(
        self, 
        command: str,
    ) -> None:

        if not isinstance(command, str):
            return

        command = command.strip()

        if not command:
            return
        
        with self.processing_lock:

            if self.processing:
                return

            self.processing = True

        try:

            self.last_activity = time.time()

            if self.on_status:
                self.on_status("🧠 Thinking...")

            logger.info(f"USER : {command}")

            if self.on_stream_start:
                self.on_stream_start()

            response = router.route(command)

            logger.debug(
                f"Router Response: {response!r}"
            )

            # -----------------------------
            # Local skill response
            # -----------------------------

            if response:

                response = response.strip()

                if self.on_stream_update:

                    current = ""

                    for word in response.split():

                        current += word + " "

                        self.on_stream_update(
                            current.rstrip()
                        )

                        time.sleep(0.02)

                self._handle_local_response(
                    response
                )

                return

    # Save assistant reply
                

            

        except Exception as e:

            logger.exception(e)

            error = "Sorry. Something went wrong."

            self._show_message(
                "Cipher",
                error,
            )

            self._speak_response(
                error,
            )

            if self.on_stream_finish:
                self.on_stream_finish()

        finally:
            
            with self.processing_lock:
                self.processing = False

            self._set_status("🟢 Ready")
    
        # -------------------------------------------------- #
    # Single Listen (GUI ST Button)
    # -------------------------------------------------- #

    def listen_once(self):

        logger.info("[GUI] listen_once() called")

        logger.info("Before listener.listen()")

        self._set_status("🎤 Listening...")

        try:

            text = listener.listen()

            logger.info(f"After listener.listen(): {text!r}")

            logger.debug(
                f"Speech Input: {text!r}"
            )

            if not text:

                
                self._set_status("🟢 Ready")

                return

            text = text.strip()

            
            self._show_message(
                    USER_NAME,
                    text.strip(),
                )

            self.process(text)

        except Exception as e:

            logger.exception(e)

            
            self._show_message(
                "System",
                f"Speech Error: {e}",
            )

        finally:

            self._set_status("🟢 Ready")

    # -------------------------------------------------- #
    # Main Loop
    # -------------------------------------------------- #
    
    def _startup(
        self,
    ) -> None:

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

        self._set_status("🟢 Online")


    def _start_processing_thread(
        self,
        command: str,
    ) -> None:

        if not self.running:
            return

        worker = threading.Thread(
            target=self.process,
            args=(command,),
            daemon=True,
            name="CipherCommand",
        )

        worker.start()

    def run(
        self,
    ) -> None:

        self._startup()

        self._listen_loop()
    
    def _listen_loop(
        self,
    ) -> None:

        while self.running:

            try:

                with self.state_lock:
                    active = self.active

                if active:

                    if (
                        time.time()
                        - self.last_activity
                        > SESSION_TIMEOUT
                    ):

                        self.sleep()
                        continue

                with self.processing_lock:

                    busy = self.processing

                if busy:

                    time.sleep(0.1)

                    continue


                text = listener.listen()

                if not text:
                    continue

                text = " ".join(text.lower().split())

                # Wake Mode

                if not active:

                    if wakeword.detect(text):

                        command = wakeword.remove(
                            text
                        )

                        self.activate()

                        if command:

                            self._start_processing_thread(
                                command
                            )

                        continue

            
                # Exit

                if text in EXIT_COMMANDS:

                    self._handle_exit()

                    break

                # Sleep

                if self._is_sleep_command(text):

                    self.sleep()

                    continue

                self._start_processing_thread(
                    text
                )

            except KeyboardInterrupt:

                self.stop()
                break

            except Exception as e:

                logger.exception(e)

                time.sleep(1)


    def _handle_exit(
        self,
    ) -> None:

        self._speak_response(
            "Goodbye."
        )

        self.stop()

    def _is_sleep_command(
        self,
        text: str,
    ) -> bool:

        return text in (
            "sleep",
            "go to sleep",
            "stop listening",
        )