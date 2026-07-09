from __future__ import annotations

import re
from pathlib import Path


class ChatValidationService:
    """
    Validates chat input and attachments.

    This service performs lightweight validation only.
    It does not modify or process the content.
    """

    MAX_MESSAGE_LENGTH = 100_000

    # --------------------------------------------------

    def validate_message(
        self,
        text: str,
    ) -> tuple[bool, str]:

        if text is None:
            return False, "Message cannot be None."

        text = text.strip()

        if not text:
            return False, "Message is empty."

        if len(text) > self.MAX_MESSAGE_LENGTH:
            return (
                False,
                f"Message exceeds {self.MAX_MESSAGE_LENGTH} characters.",
            )

        return True, ""

    # --------------------------------------------------

    def validate_filename(
        self,
        filename: str,
    ) -> tuple[bool, str]:

        if not filename:
            return False, "Filename is empty."

        if re.search(r'[<>:"|?*]', filename):
            return False, "Filename contains invalid characters."

        return True, ""

    # --------------------------------------------------

    def validate_path(
        self,
        path: str | Path,
    ) -> tuple[bool, str]:

        path = Path(path)

        if not path.exists():
            return False, "File does not exist."

        if not path.is_file():
            return False, "Path is not a file."

        return True, ""

    # --------------------------------------------------

    def validate_extension(
        self,
        path: str | Path,
        allowed_extensions: set[str],
    ) -> tuple[bool, str]:

        extension = Path(path).suffix.lower()

        if extension not in allowed_extensions:
            return (
                False,
                f"Unsupported file type: {extension}",
            )

        return True, ""

    # --------------------------------------------------

    def sanitize_text(
        self,
        text: str,
    ) -> str:

        return re.sub(
            r"\s+",
            " ",
            text.strip(),
        )


chat_validation_service = ChatValidationService()