import asyncio
import os
import queue
import subprocess
import tempfile
import threading

import edge_tts

from core.logger import logger
from config import VOICE

try:
    from core.listener import (
        pause_listening,
        resume_listening,
    )
except Exception:

    def pause_listening():
        pass

    def resume_listening():
        pass


class Speaker:

    def __init__(self):

        self.queue = queue.Queue()

        self.running = True

        # GUI callbacks
        self.on_start = None
        self.on_finish = None
        self.on_error = None

        self.thread = threading.Thread(
            target=self._worker,
            daemon=True,
        )

        self.thread.start()
        self.player = None

    # --------------------------------------------------

    def speak(self, text):

        if not text:
            return

        text = str(text).strip()

        if not text:
            return

        self.queue.put(text)

    # --------------------------------------------------

    def stop(self):

        self.stop_speaking()

        self.running = False

        self.clear_queue()

        if self.player:

            try:

                self.player.terminate()

                self.player.wait(timeout=1)

            except Exception:

                pass

            self.player = None
        self.queue.put(None)

    # --------------------------------------------------

    def clear_queue(self):

        while not self.queue.empty():
            try:
                self.queue.get_nowait()
            except queue.Empty:
                break


    def stop_speaking(self):
        """
        Stop the current speech without shutting down
        the speaker thread.
        """

        self.clear_queue()

        if self.player:

            try:
                self.player.terminate()
                self.player.wait(timeout=1)

            except Exception:
                pass

            self.player = None
    # --------------------------------------------------

    @property
    def is_speaking(self):

        return (
            self.player is not None
            or not self.queue.empty()
        )

    # --------------------------------------------------

    def _worker(self):

        while self.running:

            text = self.queue.get()

            if text is None:
                break

            try:

                if self.on_start:
                    self.on_start(text)

                pause_listening()

                asyncio.run(
                    self._tts(text)
                )

            except Exception as e:

                logger.exception(e)

                if self.on_error:
                    self.on_error(str(e))

            finally:

                resume_listening()

                if self.on_finish:
                    self.on_finish()

    # --------------------------------------------------

    async def _tts(self, text):

        with tempfile.NamedTemporaryFile(
            suffix=".mp3",
            delete=False,
        ) as file:

            filename = file.name

        try:

            communicate = edge_tts.Communicate(
                text=text,
                voice=VOICE,
            )

            await communicate.save(filename)

            self.player = subprocess.Popen(
                [
                    "ffplay",
                    "-nodisp",
                    "-autoexit",
                    "-loglevel",
                    "quiet",
                    filename,
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            self.player.wait()

            self.player = None


            if os.path.exists(filename):
                os.remove(filename)

        except Exception as e:
            logger.exception(e)


speaker = Speaker()