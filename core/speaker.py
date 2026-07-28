import asyncio
import queue
import subprocess
import tempfile
import threading

import edge_tts

from pathlib import Path
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

    def __init__(
       self,
    ) -> None:

        self.queue = queue.Queue()

        self.running = True

        # GUI callbacks
        self.on_start = None
        self.on_finish = None
        self.on_error = None

        self.thread = threading.Thread(
            target=self._worker,
            daemon=True,
            name="SpeakerThread",
        )

        self.thread.start()
        self.player = None
        self.player_lock = threading.Lock()

    # --------------------------------------------------

    def speak(
        self, 
        text: str,
    ) -> None:
        
        if text is None:
            return

        text = str(text).strip()

        if not text:
            return

        self.queue.put(text)

    def _play_audio(
        self,
        filename: str,
    ) -> None:

        with self.player_lock:

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

    # --------------------------------------------------

    def stop(
        self,
    ) -> None:

        if not self.running:
            return

        self.stop_speaking()

        self.running = False

        self.clear_queue()

        if self.player:

            try:

                self.player.terminate()

                self.player.wait(timeout=1)

            except Exception:

                logger.exception(
                    "[SPEAKER] Failed to stop player."
                )

            self.player = None
        self.queue.put(None)

    # --------------------------------------------------

    def clear_queue(
        self,
    ) -> None:

        while not self.queue.empty():
            try:
                self.queue.get_nowait()
            except queue.Empty:
                break


    def stop_speaking(
        self
    ) -> None:
        """
        Stop the current speech without shutting down
        the speaker thread.
        """

        self.clear_queue()

        with self.player_lock:

            if self.player:

                try:
                    self.player.terminate()
                    self.player.wait(timeout=2)

                except Exception:

                    logger.exception(
                        "[SPEAKER] Failed to stop player."
                    )

                self.player = None

    def _delete_temp_file(
        self,
        filename: str,
    ) -> None:

        path = Path(filename)

        try:
            if path.exists():
                path.unlink()

        except Exception:

            logger.warning(
                "[SPEAKER] Failed to delete temporary audio file."
            )
    # --------------------------------------------------



    @property
    def is_speaking(
        self,
    ) -> bool:

        with self.player_lock:

            speaking = (
                self.player is not None
                and self.player.poll() is None
            )

        return speaking or not self.queue.empty()

    # --------------------------------------------------

    def _worker(
        self,
    ) -> None:

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

                logger.exception(
                    "[SPEAKER] Worker failed."
                )

                if self.on_error:
                    self.on_error(str(e))

            finally:

                resume_listening()

                if self.on_finish:
                    self.on_finish()

    # --------------------------------------------------

    async def _tts(
        self, 
        text: str,
    ) -> None:

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

            self._play_audio(
                filename,
            )

        except Exception:

            logger.exception(
                "[SPEAKER] TTS playback failed."
            )

        finally:

            self.player = None

            self._delete_temp_file(
                filename,
            )

        


speaker = Speaker()