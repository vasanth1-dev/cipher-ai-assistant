from __future__ import annotations

import importlib
from pathlib import Path
from types import ModuleType
from typing import Optional

from core.logger import logger


class PluginLoader:
    """
    Responsible for importing and reloading plugin modules.

    This class only deals with Python module loading.
    Registration and lifecycle management are handled by
    PluginRegistry and PluginManager.
    """

    # --------------------------------------------------
    # Import
    # --------------------------------------------------

    @staticmethod
    def import_module(module_name: str) -> Optional[ModuleType]:

        try:

            module = importlib.import_module(module_name)

            logger.info(
                f"Imported plugin module: {module_name}"
            )

            return module

        except Exception as e:

            logger.exception(
                f"Failed importing '{module_name}': {e}"
            )

            return None

    # --------------------------------------------------
    # Reload
    # --------------------------------------------------

    @staticmethod
    def reload_module(module: ModuleType) -> Optional[ModuleType]:

        try:

            module = importlib.reload(module)

            logger.info(
                f"Reloaded plugin module: {module.__name__}"
            )

            return module

        except Exception as e:

            logger.exception(
                f"Failed reloading '{module.__name__}': {e}"
            )

            return None

    # --------------------------------------------------
    # Module Name
    # --------------------------------------------------

    @staticmethod
    def module_name(
        plugin_directory: Path,
        root_package: str = "plugins.available",
    ) -> str:
        """
        Convert a plugin directory into a Python module path.

        Example

        plugins/available/weather
            ->
        plugins.available.weather
        """

        return f"{root_package}.{plugin_directory.name}"