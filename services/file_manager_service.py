from __future__ import annotations

from pathlib import Path


class FileManagerService:
    """
    Placeholder File Manager Service.

    This service will later support:
    - List files
    - Create files
    - Delete files
    - Rename files
    - Copy and move files
    """

    def list_files(self, directory: str = ".") -> list[str]:
        try:
            return [item.name for item in Path(directory).iterdir()]
        except Exception:
            return []

    def execute(self, command: str) -> str:
        command = command.strip()

        if not command:
            return "Please provide a file manager command."

        return f"File Manager service is not implemented yet. Command: {command}"


file_manager_service = FileManagerService()