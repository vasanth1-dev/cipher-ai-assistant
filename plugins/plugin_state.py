from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class PluginStatus(str, Enum):
    """
    Runtime state of a plugin.
    """

    DISCOVERED = "discovered"
    REGISTERED = "registered"
    LOADED = "loaded"
    ENABLED = "enabled"
    DISABLED = "disabled"
    ERROR = "error"
    UNLOADED = "unloaded"


@dataclass(slots=True)
class PluginState:
    """
    Stores runtime information about a plugin.

    This class is intentionally independent of the plugin
    implementation so the manager/registry can track plugin
    lifecycle without modifying plugin objects.
    """

    name: str

    status: PluginStatus = PluginStatus.DISCOVERED

    enabled: bool = True

    loaded_at: Optional[datetime] = None

    unloaded_at: Optional[datetime] = None

    last_error: Optional[str] = None

    metadata: dict = field(default_factory=dict)

    # --------------------------------------------------
    # Lifecycle
    # --------------------------------------------------

    def mark_registered(self) -> None:

        self.status = PluginStatus.REGISTERED

    def mark_loaded(self) -> None:

        self.status = PluginStatus.LOADED
        self.loaded_at = datetime.utcnow()
        self.last_error = None

    def mark_enabled(self) -> None:

        self.enabled = True
        self.status = PluginStatus.ENABLED

    def mark_disabled(self) -> None:

        self.enabled = False
        self.status = PluginStatus.DISABLED

    def mark_unloaded(self) -> None:

        self.status = PluginStatus.UNLOADED
        self.unloaded_at = datetime.utcnow()

    def mark_error(
        self,
        error: Exception | str,
    ) -> None:

        self.status = PluginStatus.ERROR
        self.last_error = str(error)

    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------

    def set(
        self,
        key: str,
        value,
    ) -> None:

        self.metadata[key] = value

    def get(
        self,
        key: str,
        default=None,
    ):

        return self.metadata.get(key, default)

    # --------------------------------------------------
    # Serialization
    # --------------------------------------------------

    def to_dict(self) -> dict:

        return {
            "name": self.name,
            "status": self.status.value,
            "enabled": self.enabled,
            "loaded_at": (
                self.loaded_at.isoformat()
                if self.loaded_at
                else None
            ),
            "unloaded_at": (
                self.unloaded_at.isoformat()
                if self.unloaded_at
                else None
            ),
            "last_error": self.last_error,
            "metadata": dict(self.metadata),
        }