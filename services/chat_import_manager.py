from __future__ import annotations

import json
from pathlib import Path


class ChatImportManager:
    """
    Imports conversations from external files.

    Currently supported:
    - TXT
    - JSON

    Future:
    - Markdown
    - HTML
    - PDF
    """

    # --------------------------------------------------

    def import_txt(
        self,
        filepath: str | Path,
    ) -> list[dict]:

        path = Path(filepath)

        with open(
            path,
            "r",
            encoding="utf-8",
        ) as file:

            text = file.read()

        return [
            {
                "role": "system",
                "content": text,
            }
        ]

    # --------------------------------------------------

    def import_json(
        self,
        filepath: str | Path,
    ) -> list[dict]:

        path = Path(filepath)

        with open(
            path,
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

        if isinstance(data, dict):
            return data.get("messages", [])

        if isinstance(data, list):
            return data

        return []

    # --------------------------------------------------

    def supported_extensions(self):

        return (
            ".txt",
            ".json",
        )

    # --------------------------------------------------

    def is_supported(
        self,
        filepath: str | Path,
    ) -> bool:

        return (
            Path(filepath).suffix.lower()
            in self.supported_extensions()
        )


chat_import_manager = ChatImportManager()