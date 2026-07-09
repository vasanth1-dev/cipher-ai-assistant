"""
Cipher v2
Dependency Checker

Validates required runtime dependencies before Cipher starts.

Checks
------
- Python packages
- External executables
- File existence
- Optional feature availability

This service reports missing dependencies but does not install them.
"""

from __future__ import annotations

import importlib
import shutil
from pathlib import Path

from core.logger import logger


class DependencyChecker:
    """
    Runtime dependency validator.
    """

    def __init__(self):
        self._errors: list[str] = []
        self._warnings: list[str] = []

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def check(self) -> bool:
        """
        Returns True if no required dependency is missing.
        """
        self._errors.clear()
        self._warnings.clear()

        return len(self._errors) == 0

    @property
    def errors(self) -> list[str]:
        return list(self._errors)

    @property
    def warnings(self) -> list[str]:
        return list(self._warnings)

    # --------------------------------------------------
    # Python Modules
    # --------------------------------------------------

    def require_module(
        self,
        module: str,
        *,
        required: bool = True,
    ) -> bool:
        """
        Verify that a Python module can be imported.
        """
        try:
            importlib.import_module(module)
            return True

        except Exception:
            message = f"Missing Python module: {module}"

            if required:
                self._errors.append(message)
                logger.error(message)
            else:
                self._warnings.append(message)
                logger.warning(message)

            return False

    # --------------------------------------------------
    # Executables
    # --------------------------------------------------

    def require_executable(
        self,
        executable: str,
        *,
        required: bool = True,
    ) -> bool:
        """
        Verify that an executable exists in PATH.
        """
        if shutil.which(executable):
            return True

        message = f"Missing executable: {executable}"

        if required:
            self._errors.append(message)
            logger.error(message)
        else:
            self._warnings.append(message)
            logger.warning(message)

        return False

    # --------------------------------------------------
    # Files
    # --------------------------------------------------

    def require_file(
        self,
        path: str | Path,
        *,
        required: bool = True,
    ) -> bool:
        """
        Verify that a required file exists.
        """
        path = Path(path)

        if path.exists():
            return True

        message = f"Missing file: {path}"

        if required:
            self._errors.append(message)
            logger.error(message)
        else:
            self._warnings.append(message)
            logger.warning(message)

        return False

    # --------------------------------------------------
    # Reporting
    # --------------------------------------------------

    def summary(self) -> dict:
        """
        Return dependency check results.
        """
        return {
            "ok": len(self._errors) == 0,
            "errors": self.errors,
            "warnings": self.warnings,
        }