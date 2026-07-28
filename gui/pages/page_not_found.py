from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from gui.theme import (
    BACKGROUND,
    PRIMARY,
    PRIMARY_HOVER,
    TEXT,
    TEXT_MUTED,
)


class PageNotFound(QWidget):

     def __init__(
       self,
    ) -> None:
        super().__init__()

        self._build_ui()

    def _build_ui(
        self,
    ) -> None:

        self.setStyleSheet(f"""
        QWidget {{
            background:{BACKGROUND};
            color:{TEXT};
        }}

        QPushButton {{
            background:{PRIMARY};
            color:white;
            border:none;
            border-radius:10px;
            padding:12px 20px;
            font-weight:bold;
        }}

        QPushButton:hover {{
            background:{PRIMARY_HOVER};
        }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(18)

        layout.addStretch()

        title = QLabel("404")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
        font-size:48px;
        font-weight:bold;
        """)

        subtitle = QLabel("Page Not Found")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("""
        font-size:22px;
        font-weight:bold;
        """)

        description = QLabel(
            "The requested page is not available yet."
        )
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setWordWrap(True)
        description.setStyleSheet(f"""
        color:{TEXT_MUTED};
        font-size:11pt;
        """)

        self.home_button = QPushButton("Go to Dashboard")
        self.home_button.setFixedWidth(180)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(description, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(
            self.home_button,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )

        layout.addStretch()