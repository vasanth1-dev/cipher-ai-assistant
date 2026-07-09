"""
Cipher v2
Clipboard Monitor Service

Monitors the system clipboard and feeds new clipboard entries
into the Clipboard History plugin.

This service is intentionally separated from the plugin so that
clipboard monitoring can run continuously in the background while
the plugin remains a reusable data manager.
"""

from __future__ import annotations

import threading
import time
from typing import Optional

from core.logger import logger

try:
    import pyperclip
except ImportError:
    pyperclip = None


class ClipboardMonitor:
    """
    Background clipboard monitor.
    """

    def __init__(
        self,
        history_plugin,
        interval: float = 0.5,
    ):
        self.history_plugin = history_plugin
        self.interval = max(0.1, interval)

        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._last_text = ""

    # --------------------------------------------------
    # Lifecycle
    # --------------------------------------------------

    def start(self):
        if self._running:
            return

        self._require_dependency()

        self._running = True

        self._thread = threading.Thread(
            target=self._run,
            name="ClipboardMonitor",
            daemon=True,
        )

        self._thread.start()

        logger.info("Clipboard monitor started.")

    def stop(self):
        self._running = False

        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2)

        logger.info("Clipboard monitor stopped.")

    @property
    def running(self) -> bool:
        return self._running

    # --------------------------------------------------
    # Worker
    # --------------------------------------------------

    def _run(self):
        while self._running:
            try:
                text = pyperclip.paste()

                if (
                    isinstance(text, str)
                    and text
                    and text != self._last_text
                ):
                    self._last_text = text
                    self.history_plugin.add(text)

            except Exception as exc:
                logger.exception(exc)

            time.sleep(self.interval)

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    @staticmethod
    def _require_dependency():
        if pyperclip is None:
            raise RuntimeError(
                "pyperclip is not installed. "
                "Install it using: pip install pyperclip"
            )