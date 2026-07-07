from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
)


class MetricCard(QFrame):
    """
    Compact dashboard metric card.

    Examples:
        CPU        18%
        RAM       4.2 GB
        Disk       62%
        Network   Online
    """

    def __init__(
        self,
        title: str,
        value: str = "--",
        icon: str = "📊",
    ):
        super().__init__()

        self.setObjectName("MetricCard")

        self.setMinimumHeight(95)

        self.setStyleSheet("""
        QFrame#MetricCard{
            background:#1F2937;
            border:1px solid #374151;
            border-radius:12px;
        }

        QLabel{
            background:transparent;
            color:white;
        }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(15)

        self.icon_label = QLabel(icon)
        self.icon_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self.icon_label.setFixedWidth(42)
        self.icon_label.setStyleSheet("""
        font-size:20pt;
        """)

        right = QVBoxLayout()
        right.setSpacing(3)

        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("""
        color:#9CA3AF;
        font-size:10pt;
        """)

        self.value_label = QLabel(value)
        self.value_label.setStyleSheet("""
        color:white;
        font-size:16pt;
        font-weight:bold;
        """)

        right.addWidget(self.title_label)
        right.addWidget(self.value_label)

        layout.addWidget(self.icon_label)
        layout.addLayout(right)

    # --------------------------------------------------

    def set_title(self, text: str):
        self.title_label.setText(str(text))

    def set_value(self, text: str):
        self.value_label.setText(str(text))

    def set_icon(self, icon: str):
        self.icon_label.setText(str(icon))

    def set_value_color(self, color: str):
        self.value_label.setStyleSheet(f"""
        color:{color};
        font-size:16pt;
        font-weight:bold;
        """)