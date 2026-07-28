from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QPushButton,
    QWidget,
)

from gui.theme import (
    get_button_style,
)



class IconButton(QPushButton):
    """
    Reusable icon button.

    Examples
    --------
    🎤 Start Listening
    💬 New Chat
    📁 Files
    ⚙ Settings
    """

    def __init__(
        self,
        icon: str,
        text: str,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self._icon = icon
        self._text = text

        if text:
            self.setText(
                f"{icon}  {text}"
            )
        else:
            self.setText(icon)

        self.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.setMinimumHeight(48)

        if text:
            self.setMinimumWidth(110)
        else:
            self.setFixedSize(52, 52)

        self.setStyleSheet(
            get_button_style()
        )

    # ----------------------------------------

    def set_icon(
        self,
        icon: str,
    ) -> None:

        self._icon = icon

        if self._text:
            self.setText(
                f"{self._icon}  {self._text}"
            )
        else:
            self.setText(
                self._icon
            )

    def set_text(
        self,
        text: str,
    ) -> None:

        self._text = text

        if self._text:
            self.setText(
                f"{self._icon}  {self._text}"
            )
        else:
            self.setText(
                self._icon
            )

    # ----------------------------------------

    def icon(self) -> str:
        return self._icon

    def text_value(self) -> str:
        return self._text