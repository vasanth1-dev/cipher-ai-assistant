from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
)


class DashboardCard(QFrame):
    """
    Reusable dashboard card for Cipher v2.

    Example:
        CPU
        12%
        Normal
    """

    def __init__(
        self,
        title: str,
        value: str = "--",
        subtitle: str = "",
    ):
        super().__init__()

        self.setObjectName("DashboardCard")

        self.setMinimumSize(220, 150)

        self.setStyleSheet("""
        QFrame#DashboardCard{
            background:#1F2937;
            border:1px solid #374151;
            border-radius:14px;
        }

        QLabel{
            color:white;
            background:transparent;
        }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(10)

        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("""
        font-size:11pt;
        font-weight:bold;
        color:#D1D5DB;
        """)

        self.value_label = QLabel(value)
        self.value_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self.value_label.setStyleSheet("""
        font-size:28pt;
        font-weight:bold;
        color:white;
        """)

        self.subtitle_label = QLabel(subtitle)
        self.subtitle_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self.subtitle_label.setStyleSheet("""
        font-size:10pt;
        color:#9CA3AF;
        """)

        layout.addWidget(self.title_label)
        layout.addStretch()
        layout.addWidget(self.value_label)
        layout.addWidget(self.subtitle_label)
        layout.addStretch()

    # --------------------------------------------------

    def set_title(self, text: str):
        self.title_label.setText(str(text))

    def set_value(self, text: str):
        self.value_label.setText(str(text))

    def set_subtitle(self, text: str):
        self.subtitle_label.setText(str(text))

    def set_status_color(self, color: str):
        """
        Example:
            '#22C55E'
            '#F59E0B'
            '#EF4444'
        """
        self.value_label.setStyleSheet(f"""
        font-size:28pt;
        font-weight:bold;
        color:{color};
        """)