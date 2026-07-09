from __future__ import annotations

import mimetypes
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class ChatAttachment:
    """
    Metadata describing an attached file.
    """

    name: str
    path: str
    size: int
    mime_type: str
    extension: str


class ChatAttachmentService:
    """
    Handles attachment metadata.

    This service does NOT upload, parse or process files.
    It only provides information about them.
    """

    # --------------------------------------------------

    def create(
        self,
        filepath: str | Path,
    ) -> ChatAttachment:

        path = Path(filepath)

        mime_type, _ = mimetypes.guess_type(path)

        return ChatAttachment(
            name=path.name,
            path=str(path.resolve()),
            size=path.stat().st_size if path.exists() else 0,
            mime_type=mime_type or "application/octet-stream",
            extension=path.suffix.lower(),
        )

    # --------------------------------------------------

    def exists(
        self,
        filepath: str | Path,
    ) -> bool:

        return Path(filepath).exists()

    # --------------------------------------------------

    def is_text(
        self,
        filepath: str | Path,
    ) -> bool:

        mime_type, _ = mimetypes.guess_type(filepath)

        return (
            mime_type is not None
            and mime_type.startswith("text/")
        )

    # --------------------------------------------------

    def is_image(
        self,
        filepath: str | Path,
    ) -> bool:

        mime_type, _ = mimetypes.guess_type(filepath)

        return (
            mime_type is not None
            and mime_type.startswith("image/")
        )

    # --------------------------------------------------

    def readable_size(
        self,
        size: int,
    ) -> str:

        units = (
            "B",
            "KB",
            "MB",
            "GB",
            "TB",
        )

        value = float(size)

        for unit in units:

            if value < 1024 or unit == units[-1]:
                return f"{value:.1f} {unit}"

            value /= 1024


chat_attachment_service = ChatAttachmentService()