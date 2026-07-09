"""
Cipher v2
Plugin Manager

Responsible for discovering, loading, unloading, and managing
Cipher plugins.

Expected plugin interface
-------------------------

class ExamplePlugin(Plugin):
    name = "example"

    def can_handle(...):
        ...

    def handle(...):
        ...

Optional lifecycle methods:

    initialize()
    shutdown()
"""

from __future__ import annotations

import importlib
import inspect
import pkgutil
from pathlib import Path
from types import ModuleType
from typing import Any

from core.logger import logger
from plugins.base_plugin import BasePlugin


class PluginManager:
    """
    Discovers and manages Cipher plugins.
    """

    def __init__(self):
        self._plugins: dict[str, BasePlugin] = {}
        self._modules: dict[str, ModuleType] = {}

    # --------------------------------------------------
    # Discovery
    # --------------------------------------------------

    def discover(
        self,
        package: str = "plugins.available",
    ) -> list[str]:
        """
        Discover plugin packages.

        Returns a list of discovered module names.
        """
        discovered: list[str] = []

        root = importlib.import_module(package)

        for module in pkgutil.iter_modules(root.__path__):
            discovered.append(f"{package}.{module.name}")

        discovered.sort()

        return discovered

    # --------------------------------------------------
    # Loading
    # --------------------------------------------------

    def load_all(
        self,
        package: str = "plugins.available",
    ) -> list[str]:
        """
        Discover and load every available plugin.
        """
        loaded = []

        for module_name in self.discover(package):
            try:
                plugin = self.load(module_name)

                if plugin is not None:
                    loaded.append(plugin.name)

            except Exception:
                logger.exception(
                    "Failed to load plugin module: %s",
                    module_name,
                )

        return loaded

    def load(
        self,
        module_name: str,
    ) -> BasePlugin | None:
        """
        Load a single plugin module.
        """
        module = importlib.import_module(module_name)

        plugin = self._instantiate(module)

        if plugin is None:
            logger.warning(
                "No plugin class found in %s",
                module_name,
            )
            return None

        if plugin.name in self._plugins:
            logger.warning(
                "Plugin already loaded: %s",
                plugin.name,
            )
            return self._plugins[plugin.name]

        if hasattr(plugin, "initialize"):
            plugin.initialize()

        self._plugins[plugin.name] = plugin
        self._modules[plugin.name] = module

        logger.info("Loaded plugin: %s", plugin.name)

        return plugin

    # --------------------------------------------------
    # Unloading
    # --------------------------------------------------

    def unload(self, name: str) -> bool:
        plugin = self._plugins.pop(name, None)
        self._modules.pop(name, None)

        if plugin is None:
            return False

        if hasattr(plugin, "shutdown"):
            try:
                plugin.shutdown()
            except Exception:
                logger.exception(
                    "Error shutting down plugin %s",
                    name,
                )

        logger.info("Unloaded plugin: %s", name)

        return True

    # --------------------------------------------------
    # Lookup
    # --------------------------------------------------

    def get(self, name: str) -> BasePlugin | None:
        return self._plugins.get(name)

    def all(self) -> list[BasePlugin]:
        return list(self._plugins.values())

    def names(self) -> list[str]:
        return sorted(self._plugins.keys())

    # --------------------------------------------------
    # Dispatch
    # --------------------------------------------------

    def find_handler(
        self,
        text: str,
    ) -> BasePlugin | None:
        """
        Return the first plugin capable of handling the request.
        """
        for plugin in self._plugins.values():
            try:
                if plugin.can_handle(text):
                    return plugin
            except Exception:
                logger.exception(
                    "Plugin '%s' failed during can_handle()",
                    plugin.name,
                )

        return None

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    @staticmethod
    def _instantiate(
        module: ModuleType,
    ) -> BasePlugin | None:
        """
        Instantiate the first Plugin subclass found.
        """
        for _, obj in inspect.getmembers(
            module,
            inspect.isclass,
        ):
            if (
                issubclass(obj, BasePlugin)
                and obj is not BasePlugin
            ):
                return obj()

        return None

    # --------------------------------------------------
    # Information
    # --------------------------------------------------

    def status(self) -> list[dict[str, Any]]:
        """
        Return plugin status information.
        """
        result = []

        for plugin in self._plugins.values():
            result.append(
                {
                    "name": plugin.name,
                    "version": getattr(plugin, "version", "Unknown"),
                    "description": getattr(
                        plugin,
                        "description",
                        "",
                    ),
                    "class": plugin.__class__.__name__,
                }
            )

        return result

    def reload(self, name: str) -> bool:
        """
        Reload a loaded plugin.
        """
        module = self._modules.get(name)

        if module is None:
            return False

        module_name = module.__name__

        self.unload(name)

        try:
            importlib.invalidate_caches()
            importlib.reload(module)
            self.load(module_name)
            return True

        except Exception:
            logger.exception(
                "Failed to reload plugin: %s",
                name,
            )
            return False