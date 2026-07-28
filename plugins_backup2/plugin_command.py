from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


CommandHandler = Callable[..., Any]


@dataclass(slots=True)
class PluginCommand:
    """
    Represents a command exposed by a plugin.

    Example
    -------
    Plugin:
        Weather

    Commands:
        weather
        weather today
        weather tomorrow
    """

    name: str

    handler: CommandHandler

    description: str = ""

    plugin: str = ""

    aliases: List[str] = field(default_factory=list)

    usage: str = ""

    category: str = "General"

    enabled: bool = True

    metadata: Dict[str, Any] = field(default_factory=dict)

    # --------------------------------------------------
    # Execute
    # --------------------------------------------------

    def execute(
        self,
        *args,
        **kwargs,
    ) -> Any:

        return self.handler(
            *args,
            **kwargs,
        )

    # --------------------------------------------------
    # Aliases
    # --------------------------------------------------

    def matches(
        self,
        command: str,
    ) -> bool:

        command = command.strip().lower()

        if command == self.name.lower():
            return True

        return command in (
            alias.lower()
            for alias in self.aliases
        )

    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------

    def set(
        self,
        key: str,
        value: Any,
    ) -> None:

        self.metadata[key] = value

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:

        return self.metadata.get(
            key,
            default,
        )

    # --------------------------------------------------
    # Serialization
    # --------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:

        return {
            "name": self.name,
            "description": self.description,
            "plugin": self.plugin,
            "aliases": list(self.aliases),
            "usage": self.usage,
            "category": self.category,
            "enabled": self.enabled,
            "metadata": dict(self.metadata),
        }