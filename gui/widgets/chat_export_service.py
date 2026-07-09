from datetime import datetime
from pathlib import Path


class ChatExportService:

    def export_txt(self, messages, filename=None):

        if filename is None:

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            filename = f"chat_{timestamp}.txt"

        path = Path(filename)

        with path.open(
            "w",
            encoding="utf-8",
        ) as file:

            file.write(
                "Cipher Conversation Export\n"
            )

            file.write("=" * 40)
            file.write("\n\n")

            for message in messages:

                sender = message.get(
                    "sender",
                    "Unknown",
                )

                text = message.get(
                    "text",
                    "",
                )

                file.write(
                    f"{sender}:\n"
                )

                file.write(text)

                file.write("\n\n")

        return str(path)


chat_export_service = ChatExportService()