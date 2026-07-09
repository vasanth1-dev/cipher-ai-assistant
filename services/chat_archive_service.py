from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


class ChatArchiveService:
    """
    Archives completed chat sessions.

    Archive metadata is stored separately from
    active chat history.
    """

    def __init__(self):

        self.archive_dir = Path("data/archive")
        self.archive_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    # --------------------------------------------------

    def archive(
        self,
        session_id: str,
        title: str,
        message_count: int,
    ):

        path = self.archive_dir / f"{session_id}.json"

        data = {
            "session_id": session_id,
            "title": title,
            "message_count": message_count,
            "archived_at": datetime.now().isoformat(),
        }

        with open(
            path,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False,
            )

    # --------------------------------------------------

    def list_archives(self):

        archives = []

        for file in sorted(
            self.archive_dir.glob("*.json"),
            reverse=True,
        ):

            try:

                with open(
                    file,
                    "r",
                    encoding="utf-8",
                ) as f:

                    archives.append(
                        json.load(f)
                    )

            except Exception:
                continue

        return archives

    # --------------------------------------------------

    def delete(
        self,
        session_id: str,
    ):

        path = self.archive_dir / f"{session_id}.json"

        if path.exists():
            path.unlink()

    # --------------------------------------------------

    def exists(
        self,
        session_id: str,
    ) -> bool:

        return (
            self.archive_dir
            / f"{session_id}.json"
        ).exists()

    # --------------------------------------------------

    def clear(self):

        for file in self.archive_dir.glob("*.json"):
            file.unlink()


chat_archive_service = ChatArchiveService()