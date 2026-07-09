"""
Cipher v2
Performance Monitor

Collects lightweight runtime performance metrics for Cipher.

Responsibilities
----------------
- Measure command execution time
- Track average response time
- Count successful and failed commands
- Maintain runtime statistics

This class is intentionally lightweight and does not perform
continuous profiling.
"""

from __future__ import annotations

import time
from contextlib import contextmanager

from core.logger import logger


class PerformanceMonitor:
    """
    Runtime performance monitor.
    """

    def __init__(self):
        self.reset()

    # --------------------------------------------------
    # Session
    # --------------------------------------------------

    def reset(self) -> None:
        self._command_count = 0
        self._success_count = 0
        self._failure_count = 0

        self._total_execution_time = 0.0
        self._last_execution_time = 0.0
        self._slowest_execution_time = 0.0

    # --------------------------------------------------
    # Recording
    # --------------------------------------------------

    def record(
        self,
        elapsed: float,
        *,
        success: bool = True,
    ) -> None:
        """
        Record a completed command.
        """
        self._command_count += 1

        if success:
            self._success_count += 1
        else:
            self._failure_count += 1

        self._last_execution_time = elapsed
        self._total_execution_time += elapsed

        if elapsed > self._slowest_execution_time:
            self._slowest_execution_time = elapsed

    @contextmanager
    def measure(self):
        """
        Context manager for measuring execution time.

        Example:

            with monitor.measure():
                pipeline.execute(...)
        """
        start = time.perf_counter()

        success = True

        try:
            yield

        except Exception:
            success = False
            raise

        finally:
            elapsed = time.perf_counter() - start
            self.record(
                elapsed,
                success=success,
            )

    # --------------------------------------------------
    # Statistics
    # --------------------------------------------------

    @property
    def average_execution_time(self) -> float:
        if self._command_count == 0:
            return 0.0

        return (
            self._total_execution_time
            / self._command_count
        )

    def statistics(self) -> dict:
        """
        Return performance statistics.
        """
        return {
            "commands": self._command_count,
            "successful": self._success_count,
            "failed": self._failure_count,
            "average_execution_time": round(
                self.average_execution_time,
                4,
            ),
            "last_execution_time": round(
                self._last_execution_time,
                4,
            ),
            "slowest_execution_time": round(
                self._slowest_execution_time,
                4,
            ),
        }

    # --------------------------------------------------
    # Logging
    # --------------------------------------------------

    def log_summary(self) -> None:
        """
        Write current performance statistics to the logger.
        """
        logger.info(
            "Performance statistics: %s",
            self.statistics(),
        )