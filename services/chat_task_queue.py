from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class ChatTask:
    """
    Represents a queued background task.
    """

    task_id: str
    task_type: str
    payload: Any
    created_at: datetime = field(
        default_factory=datetime.now
    )


class ChatTaskQueue:
    """
    Simple in-memory FIFO task queue.

    This service is independent of Qt and threading.
    It only manages queued tasks. Workers can consume
    tasks from this queue in future milestones.
    """

    def __init__(self):

        self._queue: deque[ChatTask] = deque()

    # --------------------------------------------------

    def enqueue(
        self,
        task: ChatTask,
    ):

        self._queue.append(task)

    # --------------------------------------------------

    def dequeue(self) -> ChatTask | None:

        if not self._queue:
            return None

        return self._queue.popleft()

    # --------------------------------------------------

    def peek(self) -> ChatTask | None:

        if not self._queue:
            return None

        return self._queue[0]

    # --------------------------------------------------

    def clear(self):

        self._queue.clear()

    # --------------------------------------------------

    def empty(self) -> bool:

        return len(self._queue) == 0

    # --------------------------------------------------

    def size(self) -> int:

        return len(self._queue)

    # --------------------------------------------------

    def tasks(self) -> list[ChatTask]:

        return list(self._queue)


chat_task_queue = ChatTaskQueue()