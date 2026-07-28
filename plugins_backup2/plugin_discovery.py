from __future__ import annotations

from pathlib import Path
from typing import List

from core.logger import logger


class PluginDiscovery:
    """
    Discovers plugin packages on disk.

    Expected layout:

    plugins/
        available/
            weather/
                __init__.py
            reminder/
                __init__.py
            system/
                __init__.py
    """

    def __init__(
        self,
        plugins_directory: Path,
    ):

        self.plugins_directory = Path(plugins_directory)

    # --------------------------------------------------
    # Discovery
    # --------------------------------------------------

    def discover(self) -> List[Path]:

        plugins: List[Path] = []

        if not self.plugins_directory.exists():

            logger.warning(
                f"Plugin directory not found: "
                f"{self.plugins_directory}"
            )

            return plugins

        for entry in sorted(self.plugins_directory.iterdir()):

            if not entry.is_dir():
                continue

            if entry.name.startswith("_"):
                continue

            if self._is_plugin(entry):

                plugins.append(entry)

                logger.debug(
                    f"Discovered plugin: {entry.name}"
                )

        logger.info(
            f"Discovered {len(plugins)} plugin(s)."
        )

        return plugins

    # --------------------------------------------------
    # Validation
    # --------------------------------------------------

    @staticmethod
    def _is_plugin(directory: Path) -> bool:
        """
        A valid plugin package must contain __init__.py.
        """

        return (directory / "__init__.py").exists()

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def plugin_names(self) -> List[str]:

        return [
            path.name
            for path in self.discover()
        ]

    def exists(
        self,
        name: str,
    ) -> bool:

        return (
            self.plugins_directory / name
        ).is_dir()