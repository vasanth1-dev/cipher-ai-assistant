from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from core.logger import logger


class PluginConfig:
    """
    Handles reading and writing plugin configuration.

    Expected layout:

    data/
        plugins/
            weather.json
            reminder.json
            system.json
    """

    def __init__(
        self,
        config_directory: Path,
    ):

        self.config_directory = Path(config_directory)
        self.config_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    # --------------------------------------------------
    # Paths
    # --------------------------------------------------

    def path(
        self,
        plugin_name: str,
    ) -> Path:

        return self.config_directory / f"{plugin_name}.json"

    # --------------------------------------------------
    # Load
    # --------------------------------------------------

    def load(
        self,
        plugin_name: str,
    ) -> Dict[str, Any]:

        file = self.path(plugin_name)

        if not file.exists():
            return {}

        try:

            with file.open(
                "r",
                encoding="utf-8",
            ) as f:

                data = json.load(f)

            if isinstance(data, dict):
                return data

            logger.warning(
                f"Plugin config '{plugin_name}' "
                "is not a JSON object."
            )

        except Exception:

            logger.exception(
                f"Failed loading plugin config: "
                f"{plugin_name}"
            )

        return {}

    # --------------------------------------------------
    # Save
    # --------------------------------------------------

    def save(
        self,
        plugin_name: str,
        data: Dict[str, Any],
    ) -> bool:

        file = self.path(plugin_name)

        try:

            with file.open(
                "w",
                encoding="utf-8",
            ) as f:

                json.dump(
                    data,
                    f,
                    indent=4,
                    ensure_ascii=False,
                )

            return True

        except Exception:

            logger.exception(
                f"Failed saving plugin config: "
                f"{plugin_name}"
            )

            return False

    # --------------------------------------------------
    # Delete
    # --------------------------------------------------

    def delete(
        self,
        plugin_name: str,
    ) -> bool:

        file = self.path(plugin_name)

        if not file.exists():
            return False

        try:

            file.unlink()
            return True

        except Exception:

            logger.exception(
                f"Failed deleting plugin config: "
                f"{plugin_name}"
            )

            return False

    # --------------------------------------------------
    # Exists
    # --------------------------------------------------

    def exists(
        self,
        plugin_name: str,
    ) -> bool:

        return self.path(plugin_name).exists()

    # --------------------------------------------------
    # List
    # --------------------------------------------------

    def list_configs(self) -> list[str]:

        return sorted(
            file.stem
            for file in self.config_directory.glob("*.json")
        )