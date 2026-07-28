from datetime import datetime
from pathlib import Path
from os import PathLike
from typing import Any


class ChatExportService:

    """Service for exporting chat conversations to text files."""

    def export_txt(
        self,
        messages: list[dict[str, Any]],
        filename: str | PathLike[str] | None = None,
    ) -> str:

        if filename is None:

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            filename = f"chat_{timestamp}.txt"

        path = Path(filename)

        with path.open(
            "w",
            encoding="utf-8",
        ) as output_file:

            output_file.write(
                "Cipher Conversation Export\n"
            )

            output_file.write("=" * 40)
            output_file.write("\n\n")

            for message in messages:

                sender = message.get(
                    "sender",
                    "Unknown",
                )

                text = message.get(
                    "text",
                    "",
                )

                output_file.write(
                    f"{sender}:\n"
                )

                output_file.write(text)

                output_file.write("\n\n")

        return str(path)


chat_export_service = ChatExportService()