from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class DownloadStatus(str, Enum):
    QUEUED = "queued"
    DOWNLOADING = "downloading"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass(slots=True)
class ModelDownload:
    """
    Represents a model download task.

    This service does not perform downloads.
    It only tracks download metadata.
    """

    model_name: str
    status: DownloadStatus = DownloadStatus.QUEUED
    progress: float = 0.0
    downloaded_bytes: int = 0
    total_bytes: int = 0
    speed_bytes_per_second: float = 0.0
    started_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    error: str = ""


class ModelDownloadService:
    """
    Tracks model download state.

    A future downloader (Ollama, Hugging Face, etc.)
    can update this service while downloading.
    """

    def __init__(
       self,
    ) -> None:

        self._downloads: dict[str, ModelDownload] = {}

    # --------------------------------------------------

    def create(
        self,
        model_name: str,
    ) -> ModelDownload:

        download = ModelDownload(model_name=model_name)

        self._downloads[model_name] = download

        return download

    # --------------------------------------------------

    def get(
        self,
        model_name: str,
    ) -> ModelDownload | None:

        return self._downloads.get(model_name)

    # --------------------------------------------------

    def update_progress(
        self,
        model_name: str,
        *,
        progress: float,
        downloaded_bytes: int,
        total_bytes: int,
        speed_bytes_per_second: float,
    ):

        download = self.get(model_name)

        if download is None:
            return

        download.progress = max(
            0.0,
            min(progress, 100.0),
        )

        download.downloaded_bytes = downloaded_bytes
        download.total_bytes = total_bytes
        download.speed_bytes_per_second = speed_bytes_per_second
        download.updated_at = datetime.now()

    # --------------------------------------------------

    def set_status(
        self,
        model_name: str,
        status: DownloadStatus,
        error: str = "",
    ):

        download = self.get(model_name)

        if download is None:
            return

        download.status = status
        download.error = error
        download.updated_at = datetime.now()

    # --------------------------------------------------

    def remove(
        self,
        model_name: str,
    ):

        self._downloads.pop(model_name, None)

    # --------------------------------------------------

    def list(self):

        return sorted(
            self._downloads.values(),
            key=lambda item: item.started_at,
            reverse=True,
        )

    # --------------------------------------------------

    def clear(self):

        self._downloads.clear()


model_download_service = ModelDownloadService()