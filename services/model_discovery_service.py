from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class ModelLocation:
    """
    Represents a discovered model location.
    """

    name: str
    path: str
    source: str


class ModelDiscoveryService:
    """
    Discovers locally available model directories.

    This service does not communicate with Ollama or any
    external API. It only scans configured directories.
    """

    def __init__(
       self,
    ) -> None:

        self._directories: list[Path] = []

    # --------------------------------------------------

    def add_directory(
        self,
        directory: str | Path,
    ):

        path = Path(directory)

        if path not in self._directories:
            self._directories.append(path)

    # --------------------------------------------------

    def directories(self):

        return list(self._directories)

    # --------------------------------------------------

    def discover(self) -> list[ModelLocation]:

        discovered: list[ModelLocation] = []

        for directory in self._directories:

            if not directory.exists():
                continue

            if not directory.is_dir():
                continue

            for child in directory.iterdir():

                if not child.is_dir():
                    continue

                discovered.append(
                    ModelLocation(
                        name=child.name,
                        path=str(child.resolve()),
                        source="local",
                    )
                )

        discovered.sort(
            key=lambda model: model.name.lower()
        )

        return discovered

    # --------------------------------------------------

    def clear(self):

        self._directories.clear()


model_discovery_service = ModelDiscoveryService()