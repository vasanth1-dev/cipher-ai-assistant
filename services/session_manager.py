"""
Cipher v2
Session Manager

Maintains runtime session information for the current Cipher instance.

Responsibilities
----------------
- Generate a unique session ID
- Track startup time
- Track uptime
- Store runtime mode
- Maintain restart count
- Provide session metadata
"""

from __future__ import annotations

import platform
import time
import uuid
from datetime import datetime
from typing import Any

from core.logger import logger


class SessionManager:
    """
    Runtime session manager.
    """

    def __init__(
       self,
    ) -> None:
        self._session_id = str(uuid.uuid4())
        self._startup_time = time.time()
        self._startup_timestamp = datetime.now().isoformat()

        self._mode = "normal"
        self._restart_count = 0

        self._metadata: dict[str, Any] = {}

        logger.info(f"Session started: {self._session_id}")

    # --------------------------------------------------
    # Session Information
    # --------------------------------------------------

    @property
    def session_id(self) -> str:
        return self._session_id

    @property
    def startup_timestamp(self) -> str:
        return self._startup_timestamp

    def uptime(self) -> float:
        """
        Return uptime in seconds.
        """
        return time.time() - self._startup_time

    # --------------------------------------------------
    # Mode
    # --------------------------------------------------

    def mode(self) -> str:
        return self._mode

    def set_mode(self, mode: str) -> None:
        self._mode = mode

    # --------------------------------------------------
    # Restart Tracking
    # --------------------------------------------------

    def restart_count(self) -> int:
        return self._restart_count

    def increment_restart(self) -> int:
        self._restart_count += 1
        return self._restart_count

    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------

    def set(
        self,
        key: str,
        value: Any,
    ) -> None:
        self._metadata[key] = value

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        return self._metadata.get(key, default)

    def metadata(self) -> dict[str, Any]:
        return dict(self._metadata)

    # --------------------------------------------------
    # Diagnostics
    # --------------------------------------------------

    def info(self) -> dict[str, Any]:
        """
        Return runtime session information.
        """
        return {
            "session_id": self.session_id,
            "startup": self.startup_timestamp,
            "uptime_seconds": round(self.uptime(), 2),
            "mode": self.mode(),
            "restart_count": self.restart_count(),
            "platform": platform.system(),
            "platform_release": platform.release(),
            "python_version": platform.python_version(),
            "metadata": self.metadata(),
        }