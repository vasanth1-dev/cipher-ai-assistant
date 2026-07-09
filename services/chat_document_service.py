from __future__ import annotations

from pathlib import Path


class ChatDocumentService:
    """
    Lightweight document helper.

    This service only reads plain-text based documents.
    It does not depend on the GUI or any AI model.
    """

    TEXT_EXTENSIONS = {
        ".txt",
        ".md",
        ".py",
        ".json",
        ".yaml",
        ".yml",
        ".csv",
        ".log",
        ".ini",
        ".cfg",
        ".xml",
        ".html",
        ".css",
        ".js",
        ".sql",
        ".sh",
    }

    # --------------------------------------------------

    def supported(self, filepath: str | Path) -> bool:

        return (
            Path(filepath).suffix.lower()
            in self.TEXT_EXTENSIONS
        )

    # --------------------------------------------------

    def read(
        self,
        filepath: str | Path,
        encoding: str = "utf-8",
    ) -> str:

        path = Path(filepath)

        with open(
            path,
            "r",
            encoding=encoding,
            errors="replace",
        ) as file:

            return file.read()

    # --------------------------------------------------

    def preview(
        self,
        filepath: str | Path,
        max_characters: int = 1000,
    ) -> str:

        text = self.read(filepath)

        if len(text) <= max_characters:
            return text

        return text[:max_characters].rstrip() + "\n..."

    # --------------------------------------------------

    def line_count(
        self,
        filepath: str | Path,
    ) -> int:

        return len(
            self.read(filepath).splitlines()
        )

    # --------------------------------------------------

    def character_count(
        self,
        filepath: str | Path,
    ) -> int:

        return len(
            self.read(filepath)
        )


chat_document_service = ChatDocumentService()