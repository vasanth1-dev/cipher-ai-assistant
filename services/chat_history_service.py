from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


class ChatHistoryService:
    """
    Handles saving and loading chat conversations.

    This service is independent from the GUI.
    """

    def __init__(self):
        self.history_dir = Path("data/chat_history")
        self.history_dir.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------

    def create_session(self) -> str:

        return datetime.now().strftime("%Y%m%d_%H%M%S")

    # --------------------------------------------------

    def save(
        self,
        session_id: str,
        messages: list[dict],
    ):

        path = self.history_dir / f"{session_id}.json"

        data = {
            "session_id": session_id,
            "created_at": datetime.now().isoformat(),
            "messages": messages,
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False,
            )

    # --------------------------------------------------

    def load(self, session_id: str):

        path = self.history_dir / f"{session_id}.json"

        if not path.exists():
            return []

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data.get("messages", [])

    # --------------------------------------------------

    def list_sessions(self):

        sessions = []

        for file in sorted(
            self.history_dir.glob("*.json"),
            reverse=True,
        ):
            sessions.append(file.stem)

        return sessions

    # --------------------------------------------------

    def delete(self, session_id: str):

        path = self.history_dir / f"{session_id}.json"

        if path.exists():
            path.unlink()


chat_history_service = ChatHistoryService()