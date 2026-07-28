from __future__ import annotations

from typing import Dict, List, Optional

from core.logger import logger
from plugins.plugin_command import PluginCommand


class PluginCommandRegistry:
    """
    Registry for all plugin commands.

    Responsibilities
    ----------------
    • Register commands
    • Unregister commands
    • Lookup commands
    • Execute commands
    • Alias resolution
    """

    def __init__(
       self,
    ) -> None:

        self._commands: Dict[str, PluginCommand] = {}
        self._aliases: Dict[str, str] = {}

    # --------------------------------------------------
    # Register
    # --------------------------------------------------

    def register(
        self,
        command: PluginCommand,
    ) -> None:

        name = command.name.lower().strip()

        if name in self._commands:

            logger.warning(
                f"Plugin command already exists: {name}"
            )
            return

        self._commands[name] = command

        for alias in command.aliases:

            alias = alias.lower().strip()

            if alias:

                self._aliases[alias] = name

        logger.info(
            f"Registered plugin command: {name}"
        )

    # --------------------------------------------------
    # Remove
    # --------------------------------------------------

    def unregister(
        self,
        name: str,
    ) -> bool:

        name = name.lower().strip()

        command = self._commands.pop(name, None)

        if command is None:
            return False

        aliases = [
            alias
            for alias, target in self._aliases.items()
            if target == name
        ]

        for alias in aliases:
            self._aliases.pop(alias, None)

        logger.info(
            f"Unregistered plugin command: {name}"
        )

        return True

    # --------------------------------------------------
    # Lookup
    # --------------------------------------------------

    def get(
        self,
        name: str,
    ) -> Optional[PluginCommand]:

        name = name.lower().strip()

        actual = self._aliases.get(name, name)

        return self._commands.get(actual)

    def exists(
        self,
        name: str,
    ) -> bool:

        return self.get(name) is not None

    # --------------------------------------------------
    # Execute
    # --------------------------------------------------

    def execute(
        self,
        name: str,
        *args,
        **kwargs,
    ):

        command = self.get(name)

        if command is None:

            logger.warning(
                f"Unknown plugin command: {name}"
            )

            return None

        if not command.enabled:

            logger.warning(
                f"Plugin command disabled: {name}"
            )

            return None

        logger.debug(
            f"Executing plugin command: {command.name}"
        )

        return command.execute(
            *args,
            **kwargs,
        )

    # --------------------------------------------------
    # Lists
    # --------------------------------------------------

    def commands(self) -> List[PluginCommand]:

        return sorted(
            self._commands.values(),
            key=lambda command: command.name,
        )

    def names(self) -> List[str]:

        return sorted(
            self._commands.keys(),
        )

    # --------------------------------------------------
    # Clear
    # --------------------------------------------------

    def clear(self) -> None:

        self._commands.clear()
        self._aliases.clear()

    # --------------------------------------------------
    # Count
    # --------------------------------------------------

    @property
    def count(self) -> int:

        return len(self._commands)


# Global registry
plugin_command_registry = PluginCommandRegistry()