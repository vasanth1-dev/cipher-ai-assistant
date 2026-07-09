"""
Cipher v2
Response Formatter

Standardizes responses produced by plugins, AI services, and
internal components.

Goals
-----
- Consistent response structure
- GUI-friendly output
- API-friendly output
- Logging metadata
"""

from __future__ import annotations

from datetime import datetime
from typing import Any


class ResponseFormatter:
    """
    Creates standardized Cipher responses.
    """

    DEFAULT_SOURCE = "system"

    @classmethod
    def success(
        cls,
        message: str = "",
        *,
        source: str | None = None,
        data: Any = None,
        plugin: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Build a successful response.
        """
        return cls._build(
            success=True,
            message=message,
            source=source or cls.DEFAULT_SOURCE,
            data=data,
            plugin=plugin,
            metadata=metadata,
        )

    @classmethod
    def error(
        cls,
        message: str,
        *,
        source: str | None = None,
        code: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Build an error response.
        """
        response = cls._build(
            success=False,
            message=message,
            source=source or cls.DEFAULT_SOURCE,
            metadata=metadata,
        )

        if code is not None:
            response["error_code"] = code

        return response

    @classmethod
    def _build(
        cls,
        *,
        success: bool,
        message: str,
        source: str,
        data: Any = None,
        plugin: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        response = {
            "success": success,
            "message": message,
            "source": source,
            "timestamp": datetime.now().isoformat(),
        }

        if plugin is not None:
            response["plugin"] = plugin

        if data is not None:
            response["data"] = data

        if metadata:
            response["metadata"] = dict(metadata)

        return response

    @staticmethod
    def ensure(
        response: Any,
    ) -> dict[str, Any]:
        """
        Convert arbitrary values into a standard response.
        """
        if isinstance(response, dict):
            response.setdefault("success", True)
            response.setdefault("message", "")
            response.setdefault("source", "unknown")
            response.setdefault(
                "timestamp",
                datetime.now().isoformat(),
            )
            return response

        return {
            "success": True,
            "message": str(response),
            "source": "unknown",
            "timestamp": datetime.now().isoformat(),
        }