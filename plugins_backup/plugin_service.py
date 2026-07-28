from __future__ import annotations

from abc import ABC
from typing import Any, Optional

from core.logger import logger


class PluginService(ABC):
    """
    Base class for services exposed to plugins.

    A PluginService provides a stable interface between
    Cipher's internal systems and third-party plugins.

    Examples
    --------
    - AI Service
    - TTS Service
    - STT Service
    - Memory Service
    - Notification Service
    - Settings Service
    - Clipboard Service
    """

    def __init__(
        self,
        name: str,
        version: str = "1.0.0",
    ):

        self._name = name
        self._version = version
        self._started = False

    # --------------------------------------------------
    # Lifecycle
    # --------------------------------------------------

    def start(self) -> None:

        if self._started:
            return

        self._started = True

        logger.info(
            f"Plugin service started: {self._name}"
        )

    def stop(self) -> None:

        if not self._started:
            return

        self._started = False

        logger.info(
            f"Plugin service stopped: {self._name}"
        )

    def restart(self) -> None:

        self.stop()
        self.start()

    # --------------------------------------------------
    # Information
    # --------------------------------------------------

    @property
    def name(self) -> str:

        return self._name

    @property
    def version(self) -> str:

        return self._version

    @property
    def started(self) -> bool:

        return self._started

    # --------------------------------------------------
    # Optional Health Check
    # --------------------------------------------------

    def health(self) -> dict[str, Any]:

        return {
            "name": self._name,
            "version": self._version,
            "started": self._started,
            "healthy": self._started,
        }

    # --------------------------------------------------
    # Optional Capability Lookup
    # --------------------------------------------------

    def supports(
        self,
        capability: str,
    ) -> bool:

        return hasattr(self, capability)

    # --------------------------------------------------
    # Generic Invoke
    # --------------------------------------------------

    def invoke(
        self,
        method: str,
        *args,
        **kwargs,
    ) -> Optional[Any]:

        if not hasattr(self, method):
            return None

        func = getattr(self, method)

        if not callable(func):
            return None

        return func(*args, **kwargs)