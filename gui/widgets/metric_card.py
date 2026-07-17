from PyQt6.QtCore import (
    QEasingCurve,
    QPropertyAnimation,
)
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
)

from gui.theme import (
    PRIMARY,
    SUCCESS,
    TEXT,
    TEXT_MUTED,
    CARD_PADDING,
    RADIUS_LARGE,
    SMALL_SIZE,
    HEADER_SIZE,
    SPACING,
)


class MetricCard(QFrame):
    """
    Professional Metric Card

    Features
    --------
    • Modern compact design
    • Hover animation
    • Soft shadow
    • Accent indicator
    • Compatible API
    """

    def __init__(
        self,
        title: str,
        value: str = "--",
        icon: str = "📊",
    ):
        super().__init__()

        self._accent = PRIMARY

        self.setObjectName("MetricCard")

        self.setMinimumHeight(105)

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        self.setStyleSheet(f"""
        QFrame#MetricCard{{
            background:#1F2937;
            border:1px solid #334155;
            border-radius:14px;
        }}

        QLabel{{
            background:transparent;
            color:{TEXT};
        }}
        """)

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(14)
        self.shadow.setOffset(0, 3)
        self.shadow.setColor(QColor(0, 0, 0, 80))

        self.setGraphicsEffect(self.shadow)

        self.animation = QPropertyAnimation(
            self.shadow,
            b"blurRadius",
            self,
        )

        self.animation.setDuration(150)
        self.animation.setEasingCurve(
            QEasingCurve.Type.OutCubic
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(
            CARD_PADDING,
            CARD_PADDING,
            CARD_PADDING,
            CARD_PADDING,
        )
        layout.setSpacing(
            SPACING
        )

        self.accent = QFrame()
        self.accent.setFixedWidth(5)
        self.accent.setStyleSheet(f"""
        background:{self._accent};
        border-radius:2px;
        """)

        self.icon_label = QLabel(icon)
        self.icon_label.setStyleSheet(f"""
        font-size:{HEADER_SIZE}pt;
        """)

        right = QVBoxLayout()
        right.setSpacing(4)

        self.title_label = QLabel(title)
        self.title_label.setStyleSheet(f"""
        color:{TEXT_MUTED};
        font-size:{SMALL_SIZE}pt;
        font-weight:600;
        """)

        self.value_label = QLabel(value)
        self.value_label.setStyleSheet(f"""
        color:{TEXT};
        font-size:18pt;
        font-weight:700;
        """)

        right.addWidget(self.title_label)
        right.addWidget(self.value_label)

        layout.addWidget(self.accent)
        layout.addWidget(self.icon_label)
        layout.addLayout(right)
        layout.addStretch()

    # --------------------------------------------------

    def enterEvent(self, event):

        self.animation.stop()
        self.animation.setStartValue(
            self.shadow.blurRadius()
        )
        self.animation.setEndValue(24)
        self.animation.start()

        self.setStyleSheet(f"""
        QFrame#MetricCard{{
            background:#263244;
            border:1px solid {PRIMARY};
            border-radius:{RADIUS_LARGE}px;
        }}

        QLabel{{
            background:transparent;
            color:{TEXT};
        }}
        """)

        super().enterEvent(event)

    def leaveEvent(self, event):

        self.animation.stop()
        self.animation.setStartValue(
            self.shadow.blurRadius()
        )
        self.animation.setEndValue(14)
        self.animation.start()

        self.setStyleSheet(f"""
        QFrame#MetricCard{{
            background:#1F2937;
            border:1px solid #334155;
            border-radius:14px;
        }}

        QLabel{{
            background:transparent;
            color:{TEXT};
        }}
        """)

        super().leaveEvent(event)

    # --------------------------------------------------
    # Compatible API
    # --------------------------------------------------

    def set_title(self, text: str):
        self.title_label.setText(str(text))

    def set_value(self, text: str):
        self.value_label.setText(str(text))

    def set_icon(self, icon: str):
        self.icon_label.setText(str(icon))

    def set_value_color(self, color: str):

        self._accent = color

        self.accent.setStyleSheet(f"""
        background:{color};
        border-radius:2px;
        """)

        self.value_label.setStyleSheet(f"""
        color:{color};
        font-size:18pt;
        font-weight:700;
        """)

    def set_normal(self):
        self.set_value_color(SUCCESS)

    def set_warning(self):
        self.set_value_color("#F59E0B")

    def set_error(self):
        self.set_value_color("#EF4444")