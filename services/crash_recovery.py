"""
Cipher v2
Crash Recovery Service

Provides lightweight crash recovery support.

Responsibilities
----------------
- Capture crash information
- Persist crash reports
- Restore basic runtime state
- Expose the last crash report
"""

from __future__ import annotations

import json
import traceback
from datetime import datetime
from pathlib import Path
from typing import Any

from core.logger import logger


class CrashRecovery:
    """
    Crash recovery manager.
    """

    def __init__(self, crash_directory: str | Path = "logs/crashes"):
        self.crash_directory = Path(crash_directory)
        self.crash_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    # --------------------------------------------------
    # Crash Recording
    # --------------------------------------------------

    def record(
        self,
        exception: BaseException,
        *,
        source: str = "unknown",
        metadata: dict[str, Any] | None = None,
    ) -> Path:
        """
        Persist a crash report.
        """
        timestamp = datetime.now()

        report = {
            "timestamp": timestamp.isoformat(),
            "source": source,
            "exception": exception.__class__.__name__,
            "message": str(exception),
            "traceback": traceback.format_exc(),
            "metadata": metadata or {},
        }

        filename = (
            f"crash_{timestamp.strftime('%Y%m%d_%H%M%S')}.json"
        )

        path = self.crash_directory / filename

        path.write_text(
            json.dumps(
                report,
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        logger.exception(
            "Crash report written to %s",
            path,
        )

        return path

    # --------------------------------------------------
    # Reports
    # --------------------------------------------------

    def latest_report(self) -> Path | None:
        """
        Return the newest crash report.
        """
        reports = sorted(
            self.crash_directory.glob("crash_*.json")
        )

        if not reports:
            return None

        return reports[-1]

    def load_latest(self) -> dict[str, Any] | None:
        """
        Load the newest crash report.
        """
        report = self.latest_report()

        if report is None:
            return None

        return json.loads(
            report.read_text(encoding="utf-8")
        )

    # --------------------------------------------------
    # Cleanup
    # --------------------------------------------------

    def cleanup(self, keep: int = 20) -> None:
        """
        Keep only the newest crash reports.
        """
        reports = sorted(
            self.crash_directory.glob("crash_*.json")
        )

        if len(reports) <= keep:
            return

        for report in reports[:-keep]:
            try:
                report.unlink()
            except Exception:
                logger.exception(
                    "Failed to delete crash report: %s",
                    report,
                )