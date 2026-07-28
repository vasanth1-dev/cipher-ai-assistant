"""
Cipher v2
Process Plugin

Manage running system processes.

Features
--------
- List running processes
- Search processes
- Terminate a process by PID or name
- Get process information
- CPU and memory usage
"""

from __future__ import annotations

from typing import Any

from core.logger import logger
from plugins.base_plugin import Plugin

try:
    import psutil
except ImportError:
    psutil = None


class ProcessPlugin(Plugin):
    """
    Process management plugin.
    """

    name = "process"
    version = "1.0.0"
    description = "Manage running processes."

    def can_handle(self, text: str) -> bool:
        text = text.lower()

        keywords = (
            "process",
            "task",
            "running apps",
            "running process",
            "kill process",
            "terminate process",
            "cpu usage",
            "memory usage",
        )

        return any(keyword in text for keyword in keywords)

    def handle(self, text: str):
        """
        Process operations are expected to be invoked through
        Cipher's structured intent pipeline.
        """

        return {
            "success": True,
            "message": (
                "Process plugin is available. "
                "Waiting for structured process commands."
            ),
        }

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    @staticmethod
    def _require_library():
        if psutil is None:
            raise RuntimeError(
                "psutil is not installed. "
                "Install it using: pip install psutil"
            )

    # --------------------------------------------------
    # Process Listing
    # --------------------------------------------------

    def list_processes(self) -> list[dict[str, Any]]:
        self._require_library()

        processes = []

        for proc in psutil.process_iter(
            [
                "pid",
                "name",
                "username",
                "status",
                "cpu_percent",
                "memory_percent",
            ]
        ):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return processes

    def search(self, name: str) -> list[dict[str, Any]]:
        self._require_library()

        name = name.lower()

        results = []

        for proc in self.list_processes():
            process_name = (proc.get("name") or "").lower()

            if name in process_name:
                results.append(proc)

        return results

    # --------------------------------------------------
    # Process Details
    # --------------------------------------------------

    def process_info(self, pid: int) -> dict[str, Any]:
        self._require_library()

        process = psutil.Process(pid)

        return {
            "pid": process.pid,
            "name": process.name(),
            "status": process.status(),
            "username": process.username(),
            "cpu_percent": process.cpu_percent(interval=0.1),
            "memory_percent": process.memory_percent(),
            "threads": process.num_threads(),
            "exe": process.exe(),
            "cwd": process.cwd(),
        }

    # --------------------------------------------------
    # Termination
    # --------------------------------------------------

    def terminate(self, pid: int) -> bool:
        self._require_library()

        process = psutil.Process(pid)
        process.terminate()

        return True

    def kill(self, pid: int) -> bool:
        self._require_library()

        process = psutil.Process(pid)
        process.kill()

        return True

    # --------------------------------------------------
    # Logging
    # --------------------------------------------------

    @staticmethod
    def log_error(exc: Exception):
        logger.exception(exc)