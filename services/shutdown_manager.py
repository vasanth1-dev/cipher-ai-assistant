"""
Cipher v2
Shutdown Manager

Coordinates a graceful application shutdown.

Responsibilities
----------------
- Notify components that shutdown has started
- Stop background services
- Shutdown plugins
- Persist runtime state (when supported)
- Release resources
"""

from __future__ import annotations

from core.logger import logger


class ShutdownManager:
    """
    Coordinates orderly shutdown of Cipher.
    """

    def __init__(
        self,
        *,
        service_manager=None,
        plugin_manager=None,
        conversation_manager=None,
        context_manager=None,
        event_bus=None,
    ):
        self.service_manager = service_manager
        self.plugin_manager = plugin_manager
        self.conversation_manager = conversation_manager
        self.context_manager = context_manager
        self.event_bus = event_bus

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def shutdown(self) -> bool:
        """
        Perform a graceful shutdown.

        Returns
        -------
        bool
            True if shutdown completed without fatal errors.
        """
        logger.info("Beginning graceful shutdown...")

        success = True

        try:
            self._publish_shutdown_event()
            self._shutdown_plugins()
            self._stop_services()
            self._persist_runtime_state()

            logger.info("Shutdown completed successfully.")

        except Exception:
            logger.exception("Unexpected shutdown error.")
            success = False

        return success

    # --------------------------------------------------
    # Internal
    # --------------------------------------------------

    def _publish_shutdown_event(self):
        if self.event_bus is None:
            return

        try:
            self.event_bus.publish("application.shutdown")
        except Exception:
            logger.exception(
                "Failed to publish shutdown event."
            )

    def _shutdown_plugins(self):
        if self.plugin_manager is None:
            return

        for plugin in self.plugin_manager.all():
            if not hasattr(plugin, "shutdown"):
                continue

            try:
                plugin.shutdown()
            except Exception:
                logger.exception(
                    "Plugin shutdown failed: %s",
                    plugin.name,
                )

    def _stop_services(self):
        if self.service_manager is None:
            return

        try:
            self.service_manager.stop_all()
        except Exception:
            logger.exception(
                "Failed to stop background services."
            )

    def _persist_runtime_state(self):
        """
        Persist runtime state when supported.

        Persistent storage is intentionally delegated to the
        owning managers if they expose a save() method.
        """
        for manager in (
            self.conversation_manager,
            self.context_manager,
        ):
            if manager is None:
                continue

            if hasattr(manager, "save"):
                try:
                    manager.save()
                except Exception:
                    logger.exception(
                        "Failed to persist runtime state."
                    )