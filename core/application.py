"""
Cipher v2
Application

Top-level application object.

This class owns the application runtime and exposes a simple API
used by the GUI, CLI, or other entry points.

It intentionally delegates work to the already existing runtime
services rather than implementing business logic itself.
"""

from __future__ import annotations

from core.logger import logger
from services.application_bootstrap import ApplicationBootstrap


class CipherApplication:
    """
    Main Cipher application.
    """

    def __init__(
        self,
        *,
        ai_service=None,
        tts_service=None,
        gui=None,
    ):
        self.bootstrap = ApplicationBootstrap(
            ai_service=ai_service,
            tts_service=tts_service,
            gui=gui,
        )

        self.runtime = None
        self.initialized = False

    # --------------------------------------------------
    # Lifecycle
    # --------------------------------------------------

    def initialize(self) -> bool:
        """
        Initialize the application.
        """
        if self.initialized:
            return True

        logger.info("Initializing Cipher application...")

        ok = self.bootstrap.initialize()

        if not ok:
            return False

        self.runtime = self.bootstrap.runtime()
        self.initialized = True

        logger.info("Cipher application initialized.")

        return True

    def shutdown(self) -> None:
        """
        Shutdown the application.
        """
        if not self.initialized:
            return

        logger.info("Shutting down Cipher application...")

        self.bootstrap.shutdown()

        self.initialized = False

    # --------------------------------------------------
    # Commands
    # --------------------------------------------------

    def execute(
        self,
        text: str,
        *,
        speak: bool = True,
    ):
        """
        Execute a command through the runtime pipeline.
        """
        if not self.initialized:
            raise RuntimeError(
                "CipherApplication has not been initialized."
            )

        pipeline = self.runtime["command_pipeline"]

        return pipeline.execute(
            text,
            speak=speak,
        )

    # --------------------------------------------------
    # Convenience
    # --------------------------------------------------

    @property
    def event_bus(self):
        return self.runtime["event_bus"]

    @property
    def plugin_manager(self):
        return self.runtime["plugin_manager"]

    @property
    def service_manager(self):
        return self.runtime["service_manager"]

    @property
    def application_state(self):
        return self.runtime["application_state"]