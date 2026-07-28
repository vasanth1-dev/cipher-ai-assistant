import re


class CommandParser:

    def __init__(
       self,
    ) -> None:

        self.replacements = {
            "please": "",
            "kindly": "",
            "could you": "",
            "can you": "",
            "would you": "",
            "for me": "",
        }

    def parse(self, command: str):

        if not command:
            return ""

        command = command.lower().strip()

        # Remove punctuation
        command = re.sub(r"[^\w\s]", "", command)

        # Remove polite words (word-level)
        for old, new in self.replacements.items():
            command = re.sub(rf"\b{re.escape(old)}\b", new, command)

        command = re.sub(r"\s+", " ", command).strip()

        # -------------------------
        # OPEN
        # -------------------------

        command = re.sub(r"\blaunch\b", "open", command)
        command = re.sub(r"\bstart\b", "open", command)

        # -------------------------
        # CLOSE
        # -------------------------

        command = re.sub(r"\bexit\b", "close", command)
        command = re.sub(r"\bquit\b", "close", command)

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
        # Common speech corrections
        # -------------------------

        corrections = {
            "fire fox": "firefox",
            "vs code": "vscode",
            "visual studio": "vscode",
            "google chrome": "chrome",

            # Wake word mistakes
            "safer": "cipher",
            "safe her": "cipher",
            "cypher": "cipher",
            "sifer": "cipher",
            "cifer": "cipher",
        }

        for old, new in corrections.items():
            command = re.sub(rf"\b{re.escape(old)}\b", new, command)

        return command


parser = CommandParser()