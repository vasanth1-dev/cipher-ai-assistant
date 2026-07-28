from __future__ import annotations

import importlib
import inspect
import pkgutil
from pathlib import Path
from typing import Dict, List, Optional, Type

from core.logger import logger
from plugins.base_plugin import BasePlugin
from plugins.plugin_manifest import PluginManifest


class PluginRegistry:
    """
    Discovers, loads and manages Cipher plugins.

    Responsibilities
    ----------------
    • Discover plugin packages
    • Import plugin modules
    • Register plugin classes
    • Create plugin instances
    • Enable / Disable plugins
    • Retrieve plugins by name
    """

    def __init__(
       self,
    ) -> None:

        self._plugin_classes: Dict[str, Type[BasePlugin]] = {}
        self._plugins: Dict[str, BasePlugin] = {}

    # --------------------------------------------------
    # Discovery
    # --------------------------------------------------

    def discover(
        self,
        package: str = "plugins.available",
    ) -> None:
        """
        Discover all plugins inside a package.

        Example:

        plugins/
            available/
                weather/
                reminder/
                system/
        """

        try:

            module = importlib.import_module(package)

        except Exception as e:

            logger.error(
                f"Plugin discovery failed: {e}"
            )
            return

        package_path = Path(module.__file__).parent

        for info in pkgutil.iter_modules([str(package_path)]):

            module_name = f"{package}.{info.name}"

            self.load_module(module_name)

    # --------------------------------------------------
    # Load Module
    # --------------------------------------------------

    def load_module(self, module_name: str) -> None:

        try:

            module = importlib.import_module(module_name)

        except Exception as e:

            logger.exception(
                f"Failed loading plugin module "
                f"{module_name}: {e}"
            )
            return

        for _, obj in inspect.getmembers(module, inspect.isclass):

            if obj is BasePlugin:
                continue

            if not issubclass(obj, BasePlugin):
                continue

            self.register(obj)

    # --------------------------------------------------
    # Register
    # --------------------------------------------------

    def register(
        self,
        plugin_class: Type[BasePlugin],
    ) -> None:

        try:

            plugin = plugin_class()

        except Exception as e:

            logger.exception(
                f"Plugin initialization failed: {e}"
            )
            return

        manifest = getattr(plugin, "manifest", None)

        if manifest is None:

            logger.warning(
                f"{plugin_class.__name__} "
                "does not provide a manifest."
            )
            return
        
        if not isinstance(manifest, PluginManifest):

            logger.warning(
                f"{plugin_class.__name__} "
                "provides an invalid manifest."
            )

        name = manifest.name

        self._plugin_classes[name] = plugin_class

        logger.info(
            f"Registered plugin: {name}"
        )

    # --------------------------------------------------
    # Instantiate
    # --------------------------------------------------

    def initialize(self) -> None:

        self._plugins.clear()

        for name, plugin_class in self._plugin_classes.items():

            try:

                plugin = plugin_class()

                plugin.on_load()

                self._plugins[name] = plugin

                logger.info(
                    f"Loaded plugin: {name}"
                )

            except Exception as e:

                logger.exception(
                    f"Plugin '{name}' failed "
                    f"during load: {e}"
                )

    # --------------------------------------------------
    # Shutdown
    # --------------------------------------------------

    def shutdown(self) -> None:

        for plugin in self._plugins.values():

            try:

                plugin.on_unload()

            except Exception as e:

                logger.exception(
                    f"Plugin unload failed: {e}"
                )

        self._plugins.clear()

    # --------------------------------------------------
    # Get
    # --------------------------------------------------

    def get(
        self,
        name: str,
    ) -> Optional[BasePlugin]:

        return self._plugins.get(name)

    # --------------------------------------------------
    # Exists
    # --------------------------------------------------

    def exists(
        self,
        name: str,
    ) -> bool:

        return name in self._plugins

    # --------------------------------------------------
    # Remove
    # --------------------------------------------------

    def remove(
        self,
        name: str,
    ) -> bool:

        plugin = self._plugins.get(name)

        if plugin is None:
            return False

        try:

            plugin.on_unload()

        except Exception:

            logger.exception(
                f"Failed unloading plugin '{name}'"
            )

        del self._plugins[name]

        logger.info(
            f"Removed plugin: {name}"
        )

        return True

    # --------------------------------------------------
    # Enable
    # --------------------------------------------------

    def enable(
        self,
        name: str,
    ) -> bool:

        plugin = self.get(name)

        if plugin is None:
            return False

        plugin.enabled = True

        logger.info(
            f"Enabled plugin: {name}"
        )

        return True

    # --------------------------------------------------
    # Disable
    # --------------------------------------------------

    def disable(
        self,
        name: str,
    ) -> bool:

        plugin = self.get(name)

        if plugin is None:
            return False

        plugin.enabled = False

        logger.info(
            f"Disabled plugin: {name}"
        )

        return True

    # --------------------------------------------------
    # Lists
    # --------------------------------------------------

    def names(self) -> List[str]:

        return sorted(self._plugins.keys())

    def plugins(self) -> List[BasePlugin]:

        return list(self._plugins.values())

    def manifests(self) -> List[PluginManifest]:

        return [
            plugin.manifest
            for plugin in self._plugins.values()
        ]

    # --------------------------------------------------
    # Count
    # --------------------------------------------------

    @property
    def count(self) -> int:

        return len(self._plugins)