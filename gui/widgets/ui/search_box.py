
from PyQt6.QtWidgets import (
    QLineEdit,
    QWidget,
)



class SearchBox(QLineEdit):
    """
    Reusable search box.

    Examples:
        Search conversations...
        Search files...
        Search memories...
        Search plugins...
    """

    def __init__(
        self,
        placeholder: str = "Search...",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.setPlaceholderText(placeholder)

        self.setClearButtonEnabled(True)

        self.setMinimumHeight(54)

        self.setStyleSheet(f"""
        QLineEdit {{
            background: rgba(255,255,255,0.04);
            border: 2px solid rgba(255,255,255,0.08);
            border-radius: 14px;
            padding-left: 18px;
            padding-right: 18px;
            color: white;
            font-size: 11pt;
            selection-background-color: #4F8CFF;
        }}

        QLineEdit:focus {{
            border: 2px solid #4F8CFF;
            background: rgba(255,255,255,0.06);
        }}

        QLineEdit:hover {{
            border: 2px solid rgba(79,140,255,0.60);
        }}
        """)

        self.setCursorPosition(0)

    # ------------------------------------------

    def text_value(self) -> str:
        return self.text()

    def clear_search(self) -> None:
        self.clear()

    def set_placeholder(
        self,
        text: str,
    ) -> None:
        self.setPlaceholderText(text)