from html import escape

from PyQt6.QtGui import QTextCursor
from PyQt6.QtWidgets import QTextEdit


class ChatPanel(QTextEdit):

    def __init__(self):
        super().__init__()

        self.setReadOnly(True)

        self.setStyleSheet("""
        QTextEdit{
            background:#0F172A;
            border:1px solid #334155;
            border-radius:14px;
            padding:14px;
            color:white;
            font-size:11pt;
            selection-background-color:#2563EB;
        }
        """)

    def _append_card(self, sender: str, message: str, bg: str):

        sender = escape(sender)
        message = escape(message).replace("\n", "<br>")

        html = f"""
        <div style="
            background:{bg};
            border-radius:12px;
            padding:12px;
            margin-top:10px;
        ">
            <div style="
                font-weight:bold;
                margin-bottom:6px;
                color:white;
            ">
                {sender}
            </div>

            <div style="
                color:#E5E7EB;
                line-height:1.45;
            ">
                {message}
            </div>
        </div>
        """

        self.append(html)

        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.setTextCursor(cursor)
        self.ensureCursorVisible()

    def add_user_message(self, text: str):
        self._append_card("You", text, "#2563EB")

    def add_assistant_message(self, text: str):
        self._append_card("Cipher", text, "#334155")

    def add_system_message(self, text: str):
        self._append_card("System", text, "#14532D")

    def clear_chat(self):
        self.clear()