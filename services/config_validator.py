"""
Cipher v2
Configuration Validator

Validates runtime configuration before Cipher starts.

Responsibilities
----------------
- Validate required configuration values
- Validate filesystem paths
- Validate numeric ranges
- Report configuration errors and warnings

This class only validates configuration. It does not modify it.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from core.logger import logger


class ConfigValidator:
    """
    Runtime configuration validator.
    """

    def __init__(self):
        self._errors: list[str] = []
        self._warnings: list[str] = []

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def validate(self) -> bool:
        """
        Return True when no validation errors exist.
        """
        return len(self._errors) == 0

    @property
    def errors(self) -> list[str]:
        return list(self._errors)

    @property
    def warnings(self) -> list[str]:
        return list(self._warnings)

    # --------------------------------------------------
    # Validation Helpers
    # --------------------------------------------------

    def require(
        self,
        name: str,
        value: Any,
    ) -> bool:
        """
        Ensure a required configuration value exists.
        """
        if value is None:
            self._errors.append(
                f"Missing configuration: {name}"
            )
            return False

        if isinstance(value, str) and not value.strip():
            self._errors.append(
                f"Configuration '{name}' cannot be empty."
            )
            return False

        return True

    def validate_path(
        self,
        name: str,
        path: str | Path,
        *,
        must_exist: bool = True,
    ) -> bool:
        """
        Validate a filesystem path.
        """
        path = Path(path)

        if must_exist and not path.exists():
            self._errors.append(
                f"{name}: path does not exist ({path})"
            )
            return False

        return True

    def validate_range(
        self,
        name: str,
        value: float,
        minimum: float,
        maximum: float,
    ) -> bool:
        """
        Validate a numeric range.
        """
        if minimum <= value <= maximum:
            return True

        self._errors.append(
            f"{name}: {value} is outside "
            f"the allowed range [{minimum}, {maximum}]"
        )

        return False

    def warn(
        self,
        message: str,
    ) -> None:
        """
        Record a non-fatal warning.
        """
        self._warnings.append(message)

    # --------------------------------------------------
    # Reporting
    # --------------------------------------------------

    def summary(self) -> dict[str, Any]:
        """
        Return validation results.
        """
        return {
            "valid": len(self._errors) == 0,
            "errors": self.errors,
            "warnings": self.warnings,
        }

    def log_summary(self) -> None:
        """
        Write validation results to the logger.
        """
        if not self._errors and not self._warnings:
            logger.info(
                "Configuration validation successful."
            )
            return

        for warning in self._warnings:
            logger.warning(warning)

        for error in self._errors:
            logger.error(error)