from __future__ import annotations

from datetime import datetime
from pathlib import Path


class ChatExportManager:
    """
    Exports conversations into different formats.

    Supported:
    - TXT
    - Markdown

    Additional formats (PDF, DOCX, HTML) can be
    added later without changing the public API.
    """

    def __init__(self):

        self.export_dir = Path("exports")

        self.export_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    # --------------------------------------------------

    def export_txt(
        self,
        filename: str,
        messages: list[dict],
    ) -> Path:

        path = self.export_dir / f"{filename}.txt"

        with open(
            path,
            "w",
            encoding="utf-8",
        ) as file:

            file.write(
                f"Cipher Conversation\n"
            )

            file.write(
                f"Generated: {datetime.now()}\n"
            )

            file.write(
                "-" * 60 + "\n\n"
            )

            for message in messages:

                role = message.get(
                    "role",
                    "assistant",
                ).title()

                content = message.get(
                    "content",
                    "",
                )

                file.write(
                    f"{role}:\n"
                )

                file.write(
                    content.strip()
                )

                file.write(
                    "\n\n"
                )

        return path

    # --------------------------------------------------

    def export_markdown(
        self,
        filename: str,
        messages: list[dict],
    ) -> Path:

        path = self.export_dir / f"{filename}.md"

        with open(
            path,
            "w",
            encoding="utf-8",
        ) as file:

            file.write(
                "# Cipher Conversation\n\n"
            )

            file.write(
                f"Generated: {datetime.now()}\n\n"
            )

            file.write(
                "---\n\n"
            )

            for message in messages:

                role = message.get(
                    "role",
                    "assistant",
                ).title()

                content = message.get(
                    "content",
                    "",
                )

                file.write(
                    f"## {role}\n\n"
                )

                file.write(
                    content
                )

                file.write(
                    "\n\n"
                )

        return path

    # --------------------------------------------------

    def available_formats(self):

        return (
            "txt",
            "md",
        )


chat_export_manager = ChatExportManager()