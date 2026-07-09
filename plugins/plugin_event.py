from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict


@dataclass(slots=True)
class PluginEvent:
    """
    Standard event object exchanged between plugins.

    Examples
    --------
    command.received
    speech.started
    speech.finished
    ai.response
    reminder.created
    system.shutdown
    """

    name: str

    source: str = "system"

    payload: Dict[str, Any] = field(default_factory=dict)

    timestamp: datetime = field(default_factory=datetime.utcnow)

    handled: bool = False

    cancelled: bool = False

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def stop(self) -> None:
        """
        Prevent further processing.
        """

        self.cancelled = True

    def mark_handled(self) -> None:
        """
        Mark the event as handled.
        """

        self.handled = True

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:

        return self.payload.get(key, default)

    def set(
        self,
        key: str,
        value: Any,
    ) -> None:

        self.payload[key] = value

    def to_dict(self) -> Dict[str, Any]:

        return {
            "name": self.name,
            "source": self.source,
            "payload": dict(self.payload),
            "timestamp": self.timestamp.isoformat(),
            "handled": self.handled,
            "cancelled": self.cancelled,
        }