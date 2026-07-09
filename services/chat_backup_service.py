from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path


class ChatBackupService:
    """
    Creates timestamped backups of the chat data directory.

    This service is independent of the GUI and does not
    require any integration with existing files.
    """

    def __init__(self):

        self.data_dir = Path("data")
        self.backup_dir = Path("backups")

        self.backup_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    # --------------------------------------------------

    def create_backup(self) -> Path:

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        destination = (
            self.backup_dir
            / f"chat_backup_{timestamp}"
        )

        shutil.copytree(
            self.data_dir,
            destination,
            dirs_exist_ok=True,
        )

        return destination

    # --------------------------------------------------

    def list_backups(self) -> list[Path]:

        return sorted(
            self.backup_dir.glob("chat_backup_*"),
            reverse=True,
        )

    # --------------------------------------------------

    def delete_backup(
        self,
        backup_name: str,
    ) -> bool:

        path = self.backup_dir / backup_name

        if not path.exists():
            return False

        shutil.rmtree(path)

        return True

    # --------------------------------------------------

    def latest_backup(self) -> Path | None:

        backups = self.list_backups()

        if backups:
            return backups[0]

        return None


chat_backup_service = ChatBackupService()