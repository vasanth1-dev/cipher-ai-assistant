from __future__ import annotations


class MediaService:
    """
    Placeholder Media Service.

    This service will later support:
    - Play media
    - Pause media
    - Resume media
    - Stop media
    - Next track
    - Previous track
    """

    def execute(self, command: str) -> str:
        command = command.strip()

        if not command:
            return "Please provide a media command."

        return f"Media service is not implemented yet. Command: {command}"


media_service = MediaService()