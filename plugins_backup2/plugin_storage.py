from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from core.logger import logger


class PluginStorage:
    """
    Persistent key-value storage for plugins.

    Each plugin gets its own JSON file.

    Example:

    data/
        plugins/
            storage/
                weather.json
                reminder.json
                notes.json
    """

    def __init__(
        self,
        storage_directory: Path,
    ):

        self.storage_directory = Path(storage_directory)

        self.storage_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def _path(
        self,
        plugin_name: str,
    ) -> Path:

        return (
            self.storage_directory
            / f"{plugin_name}.json"
        )

    def _load(
        self,
        plugin_name: str,
    ) -> Dict[str, Any]:

        file = self._path(plugin_name)

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

        except Exception:

            logger.exception(
                f"Failed reading plugin storage: "
                f"{plugin_name}"
            )

        return {}

    def _save(
        self,
        plugin_name: str,
        data: Dict[str, Any],
    ) -> bool:

        try:

            with self._path(plugin_name).open(
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
                f"Failed writing plugin storage: "
                f"{plugin_name}"
            )

            return False

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def get(
        self,
        plugin_name: str,
        key: str,
        default: Any = None,
    ) -> Any:

        data = self._load(plugin_name)

        return data.get(key, default)

    def set(
        self,
        plugin_name: str,
        key: str,
        value: Any,
    ) -> bool:

        data = self._load(plugin_name)

        data[key] = value

        return self._save(
            plugin_name,
            data,
        )

    def remove(
        self,
        plugin_name: str,
        key: str,
    ) -> bool:

        data = self._load(plugin_name)

        if key not in data:
            return False

        del data[key]

        return self._save(
            plugin_name,
            data,
        )

    def clear(
        self,
        plugin_name: str,
    ) -> bool:

        return self._save(
            plugin_name,
            {},
        )

    def exists(
        self,
        plugin_name: str,
        key: str,
    ) -> bool:

        data = self._load(plugin_name)

        return key in data

    def all(
        self,
        plugin_name: str,
    ) -> Dict[str, Any]:

        return self._load(plugin_name)