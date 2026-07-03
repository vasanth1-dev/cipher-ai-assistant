import re


class CommandExecutor:

    def __init__(self):

        self.aliases = {

            # ---------- Wake Word ----------
            "hey cipher": "",
            "hi cipher": "",
            "okay cipher": "",
            "hello cipher": "",

            # ---------- Browsers ----------
            "fire fox": "firefox",
            "google chrome": "chrome",

            # ---------- Editors ----------
            "vs code": "vscode",
            "visual studio code": "vscode",
            "visual studio": "vscode",
            "code editor": "vscode",

            # ---------- Whisper mistakes ----------
            "safer": "cipher",
            "safe her": "cipher",
            "save her": "cipher",
            "cypher": "cipher",
            "sifer": "cipher",
            "cifer": "cipher",

            # ---------- Commands ----------
            "shut down": "shutdown",
            "re start": "restart",
            "log out": "logout",

            # ---------- Search ----------
            "youtube search": "search youtube",
            "google search": "search google",
        }

    def normalize(self, command: str):

        if not command:
            return ""

        command = command.lower().strip()

        command = re.sub(r"\s+", " ", command)

        for old, new in self.aliases.items():
            command = command.replace(old, new)

        command = re.sub(r"\s+", " ", command).strip()

        return command


executor = CommandExecutor()