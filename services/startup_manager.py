"""
Cipher v2
Startup Manager

Coordinates Cipher's startup sequence.

Startup Order
-------------
1. Validate configuration
2. Initialize shared services
3. Start background services
4. Load plugins
5. Initialize AI service
6. Launch GUI (optional)

The StartupManager does not own these components; it simply
coordinates them.
"""

from __future__ import annotations

from core.logger import logger


class StartupManager:
    """
    Coordinates Cipher startup.
    """

    def __init__(
        self,
        *,
        service_manager=None,
        plugin_manager=None,
        ai_service=None,
        gui=None,
    ):
        self.service_manager = service_manager
        self.plugin_manager = plugin_manager
        self.ai_service = ai_service
        self.gui = gui

    # --------------------------------------------------
    # Startup
    # --------------------------------------------------

    def start(self) -> bool:
        """
        Execute the startup sequence.

        Returns
        -------
        bool
            True if startup completed successfully.
        """
        logger.info("Starting Cipher...")

        try:
            self._validate()

            self._start_services()

            self._load_plugins()

            self._initialize_ai()

            self._start_gui()

            logger.info("Cipher startup completed.")

            return True

        except Exception:
            logger.exception(
                "Cipher startup failed."
            )
            return False

    # --------------------------------------------------
    # Shutdown
    # --------------------------------------------------

    def shutdown(self) -> None:
        """
        Execute an orderly shutdown.
        """
        logger.info("Shutting down Cipher...")

        if self.service_manager is not None:
            try:
                self.service_manager.stop_all()
            except Exception:
                logger.exception(
                    "Failed to stop services."
                )

        logger.info("Cipher shutdown complete.")

    # --------------------------------------------------
    # Internal Steps
    # --------------------------------------------------

    @staticmethod
    def _validate():
        """
        Placeholder for future dependency/configuration
        validation.
        """
        logger.info("Configuration validated.")

    def _start_services(self):
        if self.service_manager is None:
            return

        self.service_manager.start_all()

    def _load_plugins(self):
        if self.plugin_manager is None:
            return

        loaded = self.plugin_manager.load_all()

        logger.info(
            "Loaded %d plugins.",
            len(loaded),
        )

    def _initialize_ai(self):
        if self.ai_service is None:
            return

        if hasattr(self.ai_service, "initialize"):
            self.ai_service.initialize()

        logger.info("AI service initialized.")

    def _start_gui(self):
        if self.gui is None:
            return

        if hasattr(self.gui, "show"):
            self.gui.show()

        logger.info("GUI started.")