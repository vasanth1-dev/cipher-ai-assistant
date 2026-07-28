from __future__ import annotations

from concurrent.futures import Future, ThreadPoolExecutor
from threading import Lock
from typing import Any, Callable, Dict, Optional

from core.logger import logger


Task = Callable[..., Any]


class PluginScheduler:
    """
    Lightweight background task scheduler for plugins.

    Responsibilities
    ----------------
    • Run plugin tasks asynchronously
    • Track running tasks
    • Cancel queued tasks
    • Gracefully shutdown worker threads

    This is intentionally lightweight. Time-based scheduling
    (cron, intervals, reminders) should be implemented by
    dedicated services, not here.
    """

    def __init__(
        self,
        max_workers: int = 4,
    ):

        self._executor = ThreadPoolExecutor(
            max_workers=max_workers,
            thread_name_prefix="PluginWorker",
        )

        self._tasks: Dict[str, Future] = {}
        self._lock = Lock()

    # --------------------------------------------------
    # Submit
    # --------------------------------------------------

    def submit(
        self,
        task_id: str,
        func: Task,
        *args,
        **kwargs,
    ) -> Future:

        future = self._executor.submit(
            func,
            *args,
            **kwargs,
        )

        with self._lock:
            self._tasks[task_id] = future

        future.add_done_callback(
            lambda _: self._cleanup(task_id)
        )

        logger.debug(
            f"Scheduled plugin task: {task_id}"
        )

        return future

    # --------------------------------------------------
    # Cancel
    # --------------------------------------------------

    def cancel(
        self,
        task_id: str,
    ) -> bool:

        with self._lock:

            future = self._tasks.get(task_id)

            if future is None:
                return False

            cancelled = future.cancel()

            if cancelled:
                self._tasks.pop(task_id, None)

            return cancelled

    # --------------------------------------------------
    # Status
    # --------------------------------------------------

    def running(
        self,
        task_id: str,
    ) -> bool:

        with self._lock:

            future = self._tasks.get(task_id)

            if future is None:
                return False

            return not future.done()

    def future(
        self,
        task_id: str,
    ) -> Optional[Future]:

        with self._lock:
            return self._tasks.get(task_id)

    # --------------------------------------------------
    # Cleanup
    # --------------------------------------------------

    def _cleanup(
        self,
        task_id: str,
    ) -> None:

        with self._lock:
            self._tasks.pop(task_id, None)

    # --------------------------------------------------
    # Information
    # --------------------------------------------------

    @property
    def active_tasks(self) -> int:

        with self._lock:

            return sum(
                not future.done()
                for future in self._tasks.values()
            )

    def task_ids(self) -> list[str]:

        with self._lock:
            return list(self._tasks.keys())

    # --------------------------------------------------
    # Shutdown
    # --------------------------------------------------

    def shutdown(
        self,
        wait: bool = True,
    ) -> None:

        logger.info(
            "Stopping Plugin Scheduler..."
        )

        self._executor.shutdown(wait=wait)

        with self._lock:
            self._tasks.clear()


# Global scheduler instance
plugin_scheduler = PluginScheduler()