from __future__ import annotations

from typing import List, Optional

from core.logger import logger
from plugins.base_plugin import BasePlugin
from plugins.plugin_registry import PluginRegistry


class PluginManager:
    """
    High-level interface for the Cipher plugin system.

    Responsibilities
    ----------------
    • Discover plugins
    • Initialize plugins
    • Shutdown plugins
    • Enable / Disable plugins
    • Access loaded plugins

    Other parts of Cipher should interact with PluginManager
    instead of PluginRegistry directly.
    """

    def __init__(
       self,
    ) -> None:

        self.registry = PluginRegistry()
        self._started = False

    # --------------------------------------------------
    # Startup
    # --------------------------------------------------

    def start(
        self,
        package: str = "plugins.available",
    ) -> None:

        if self._started:
            return

        logger.info("Starting Plugin Manager...")

        self.registry.discover(package)
        self.registry.initialize()

        self._started = True

        logger.info(
            f"Plugin Manager started "
            f"({self.registry.count} plugins loaded)"
        )

    # --------------------------------------------------
    # Shutdown
    # --------------------------------------------------

    def stop(self) -> None:

        if not self._started:
            return

        logger.info("Stopping Plugin Manager...")

        self.registry.shutdown()

        self._started = False

        logger.info("Plugin Manager stopped.")

    # --------------------------------------------------
    # Restart
    # --------------------------------------------------

    def restart(
        self,
        package: str = "plugins.available",
    ) -> None:
        
        logger.info("Restarting Plugin Manager...")

        self.stop()
        self.start(package)

    # --------------------------------------------------
    # Plugin Access
    # --------------------------------------------------

    def get(
        self,
        name: str,
    ) -> Optional[BasePlugin]:

        plugin = self.registry.get(name)

        if plugin is None:


            logger.debug(
                f"Plugin '{name}' not found."
            )
            
        return plugin

    def plugins(self) -> List[BasePlugin]:

        return self.registry.plugins()

    def names(self) -> List[str]:

        return self.registry.names()

    # --------------------------------------------------
    # Enable / Disable
    # --------------------------------------------------

    def enable(
        self,
        name: str,
    ) -> bool:

        return self.registry.enable(name)

    def disable(
        self,
        name: str,
    ) -> bool:

        return self.registry.disable(name)

    # --------------------------------------------------
    # Status
    # --------------------------------------------------

    def exists(
        self,
        name: str,
    ) -> bool:

        return self.registry.exists(name)

    @property
    def started(self) -> bool:

        return self._started

    @property
    def count(self) -> int:

        return self.registry.count


# Global instance
plugin_manager = PluginManager()