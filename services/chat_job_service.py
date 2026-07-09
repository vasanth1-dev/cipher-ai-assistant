from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import uuid4


class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass(slots=True)
class ChatJob:
    """
    Represents a background job tracked by Cipher.
    """

    job_id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    status: JobStatus = JobStatus.PENDING
    progress: int = 0
    result: object | None = None
    error: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


class ChatJobService:
    """
    Tracks background jobs.

    This service only manages job state.
    It does not execute jobs.
    """

    def __init__(self):

        self._jobs: dict[str, ChatJob] = {}

    # --------------------------------------------------

    def create(
        self,
        name: str,
    ) -> ChatJob:

        job = ChatJob(name=name)

        self._jobs[job.job_id] = job

        return job

    # --------------------------------------------------

    def get(
        self,
        job_id: str,
    ) -> ChatJob | None:

        return self._jobs.get(job_id)

    # --------------------------------------------------

    def list(self) -> list[ChatJob]:

        return sorted(
            self._jobs.values(),
            key=lambda job: job.created_at,
            reverse=True,
        )

    # --------------------------------------------------

    def update_progress(
        self,
        job_id: str,
        progress: int,
    ):

        job = self.get(job_id)

        if job is None:
            return

        job.progress = max(
            0,
            min(progress, 100),
        )

        job.updated_at = datetime.now()

    # --------------------------------------------------

    def update_status(
        self,
        job_id: str,
        status: JobStatus,
    ):

        job = self.get(job_id)

        if job is None:
            return

        job.status = status
        job.updated_at = datetime.now()

    # --------------------------------------------------

    def complete(
        self,
        job_id: str,
        result=None,
    ):

        job = self.get(job_id)

        if job is None:
            return

        job.status = JobStatus.COMPLETED
        job.progress = 100
        job.result = result
        job.updated_at = datetime.now()

    # --------------------------------------------------

    def fail(
        self,
        job_id: str,
        error: str,
    ):

        job = self.get(job_id)

        if job is None:
            return

        job.status = JobStatus.FAILED
        job.error = error
        job.updated_at = datetime.now()

    # --------------------------------------------------

    def remove(
        self,
        job_id: str,
    ):

        self._jobs.pop(job_id, None)

    # --------------------------------------------------

    def clear(self):

        self._jobs.clear()


chat_job_service = ChatJobService()