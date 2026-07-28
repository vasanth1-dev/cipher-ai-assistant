from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


class ChatMetadataService:
    """
    Stores metadata for chat sessions.

    Metadata is kept separate from the conversation
    itself so it can evolve independently.
    """

     def __init__(
       self,
    ) -> None:

        self._directory = Path("data/chat_metadata")
        self._directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    # --------------------------------------------------

    def save(
        self,
        session_id: str,
        metadata: dict,
    ):

        metadata = dict(metadata)

        metadata["updated_at"] = (
            datetime.now().isoformat()
        )

        path = self._directory / f"{session_id}.json"

        with open(
            path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                metadata,
                file,
                indent=4,
                ensure_ascii=False,
                sort_keys=True,
            )

    # --------------------------------------------------

    def load(
        self,
        session_id: str,
    ) -> dict:

        path = self._directory / f"{session_id}.json"

        if not path.exists():
            return {}

        try:

            with open(
                path,
                "r",
                encoding="utf-8",
            ) as file:

                return json.load(file)

        except Exception:
            return {}

    # --------------------------------------------------

    def delete(
        self,
        session_id: str,
    ):

        path = self._directory / f"{session_id}.json"

        if path.exists():
            path.unlink()

    # --------------------------------------------------

    def exists(
        self,
        session_id: str,
    ) -> bool:

        return (
            self._directory
            / f"{session_id}.json"
        ).exists()

    # --------------------------------------------------

    def list_sessions(self):

        return sorted(
            file.stem
            for file in self._directory.glob("*.json")
        )


chat_metadata_service = ChatMetadataService()