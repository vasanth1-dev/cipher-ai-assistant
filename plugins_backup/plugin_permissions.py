from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable, Set

from core.logger import logger


class Permission(str, Enum):
    """
    Standard permissions available to Cipher plugins.
    """

    AI = "ai"
    AUDIO = "audio"
    CAMERA = "camera"
    CLIPBOARD = "clipboard"
    FILESYSTEM = "filesystem"
    GUI = "gui"
    MEMORY = "memory"
    MICROPHONE = "microphone"
    NETWORK = "network"
    NOTIFICATIONS = "notifications"
    PROCESS = "process"
    SETTINGS = "settings"
    SHELL = "shell"
    SYSTEM = "system"
    TTS = "tts"


@dataclass(slots=True)
class PluginPermissions:
    """
    Runtime permission container for a plugin.
    """

    allowed: Set[str] = field(default_factory=set)

    # --------------------------------------------------
    # Grant
    # --------------------------------------------------

    def grant(
        self,
        permission: Permission | str,
    ) -> None:

        self.allowed.add(str(permission))

    def grant_many(
        self,
        permissions: Iterable[Permission | str],
    ) -> None:

        for permission in permissions:
            self.grant(permission)

    # --------------------------------------------------
    # Revoke
    # --------------------------------------------------

    def revoke(
        self,
        permission: Permission | str,
    ) -> None:

        self.allowed.discard(str(permission))

    # --------------------------------------------------
    # Query
    # --------------------------------------------------

    def has(
        self,
        permission: Permission | str,
    ) -> bool:

        return str(permission) in self.allowed

    def require(
        self,
        permission: Permission | str,
    ) -> bool:

        if self.has(permission):
            return True

        logger.warning(
            "Permission denied: %s",
            permission,
        )

        return False

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def clear(self) -> None:

        self.allowed.clear()

    def to_list(self) -> list[str]:

        return sorted(self.allowed)

    def __contains__(
        self,
        permission: Permission | str,
    ) -> bool:

        return self.has(permission)

    def __len__(self) -> int:

        return len(self.allowed)