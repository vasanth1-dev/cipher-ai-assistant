"""
Cipher v2
Error Handler

Centralized exception handling for the application.

Responsibilities
----------------
- Log exceptions
- Convert exceptions into user-friendly responses
- Categorize errors
- Invoke optional recovery callbacks
"""

from __future__ import annotations

import traceback
from typing import Any, Callable

from core.logger import logger


class ErrorHandler:
    """
    Centralized error handler.
    """

    def __init__(self):
        self._recovery_hooks: dict[
            type[BaseException],
            Callable[[BaseException], Any],
        ] = {}

    # --------------------------------------------------
    # Registration
    # --------------------------------------------------

    def register_recovery(
        self,
        exception_type: type[BaseException],
        callback: Callable[[BaseException], Any],
    ) -> None:
        """
        Register a recovery callback for an exception type.
        """
        self._recovery_hooks[exception_type] = callback

    # --------------------------------------------------
    # Handling
    # --------------------------------------------------

    def handle(
        self,
        exception: BaseException,
        *,
        source: str = "unknown",
    ) -> dict[str, Any]:
        """
        Handle an exception and return a standardized response.
        """
        logger.exception(
            "Unhandled exception from %s",
            source,
        )

        self._run_recovery(exception)

        return {
            "success": False,
            "source": source,
            "error_type": exception.__class__.__name__,
            "message": self._friendly_message(exception),
        }

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def _run_recovery(
        self,
        exception: BaseException,
    ) -> None:
        """
        Execute a matching recovery callback if one exists.
        """
        for exc_type, callback in self._recovery_hooks.items():
            if isinstance(exception, exc_type):
                try:
                    callback(exception)
                except Exception:
                    logger.exception(
                        "Recovery callback failed."
                    )
                break

    @staticmethod
    def _friendly_message(
        exception: BaseException,
    ) -> str:
        """
        Produce a user-friendly message.
        """
        if isinstance(exception, FileNotFoundError):
            return "The requested file could not be found."

        if isinstance(exception, PermissionError):
            return "Permission denied."

        if isinstance(exception, TimeoutError):
            return "The operation timed out."

        message = str(exception).strip()

        if message:
            return message

        return "An unexpected error occurred."

    # --------------------------------------------------
    # Diagnostics
    # --------------------------------------------------

    @staticmethod
    def traceback() -> str:
        """
        Return the current traceback as a string.
        """
        return traceback.format_exc()