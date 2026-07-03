import re


class CommandParser:

    def __init__(self):

        self.replacements = {
            # Polite words
            "please": "",
            "kindly": "",
            "could you": "",
            "can you": "",
            "would you": "",
            "for me": "",

            # Articles
            "the": "",
            "a": "",
            "an": "",
        }

    def parse(self, command: str):

        if not command:
            return ""

        command = command.lower().strip()

        # Remove punctuation
        command = re.sub(r"[^\w\s]", "", command)

        # Remove unwanted words
        for old, new in self.replacements.items():
            command = command.replace(old, new)

        command = re.sub(r"\s+", " ", command).strip()

        # -------------------------
        # OPEN
        # -------------------------

        command = command.replace("launch", "open")
        command = command.replace("start", "open")

        # -------------------------
        # CLOSE
        # -------------------------

        command = command.replace("exit", "close")
        command = command.replace("quit", "close")

        # -------------------------
        # Browser shortcuts
        # -------------------------

        if command.startswith("google "):
            query = command.replace("google", "", 1).strip()
            command = f"search google {query}"

        if command.startswith("youtube "):
            query = command.replace("youtube", "", 1).strip()
            command = f"search youtube {query}"

        # -------------------------
        # Indian English corrections
        # -------------------------

        corrections = {
            "fire fox": "firefox",
            "vs code": "vscode",
            "visual studio": "vscode",
            "google chrome": "chrome",

            # Whisper mistakes
            "safer": "cipher",
            "safe her": "cipher",
            "cypher": "cipher",
            "sifer": "cipher",
            "cifer": "cipher",
        }

        for old, new in corrections.items():
            command = command.replace(old, new)

        return command


parser = CommandParser()