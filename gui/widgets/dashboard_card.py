from PyQt6.QtCore import (
    QEasingCurve,
    QEvent,
    QPropertyAnimation,
)
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QFrame,
    QGraphicsDropShadowEffect,
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
    SPACING,
    RADIUS_LARGE,
    HEADER_SIZE,
    SMALL_SIZE,
)


class DashboardCard(QFrame):
    """
    Professional Dashboard Card

    Features
    --------
    • Modern card design
    • Hover animation
    • Soft shadow
    • Status accent
    • Compatible API
    """

    def __init__(
        self,
        title: str,
        value: str = "--",
        subtitle: str = "",
    ):
        super().__init__()

        self._accent = SUCCESS

        self.setObjectName("DashboardCard")

        self.setMinimumSize(240, 165)

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )

        self.setCursor(
            self.cursor()
        )

        self.setStyleSheet(f"""
        QFrame#DashboardCard{{
            background:#1F2937;
            border:1px solid #334155;
            border-radius:{RADIUS_LARGE}px;
        }}

        QLabel{{
            background:transparent;
            color:{TEXT};
        }}
        """)

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(18)
        self.shadow.setOffset(0, 4)
        self.shadow.setColor(
            QColor(0, 0, 0, 90)
        )

        self.setGraphicsEffect(
            self.shadow
        )

        self.animation = QPropertyAnimation(
            self.shadow,
            b"blurRadius",
            self,
        )

        self.animation.setDuration(160)
        self.animation.setEasingCurve(
            QEasingCurve.Type.OutCubic
        )

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            CARD_PADDING,
            CARD_PADDING,
            CARD_PADDING,
            CARD_PADDING,
        )

        layout.setSpacing(
            SPACING
        )

        self.title_label = QLabel(title)

        self.title_label.setStyleSheet(f"""
        font-size:{SMALL_SIZE}pt;
        font-weight:600;
        color:{TEXT_MUTED};
        """)

        self.status_indicator = QFrame()

        self.status_indicator.setFixedHeight(4)

        self.status_indicator.setStyleSheet(f"""
        background:{self._accent};
        border-radius:2px;
        """)

        self.value_label = QLabel(value)

        self.value_label.setStyleSheet(f"""
        font-size:{HEADER_SIZE}pt;
        font-weight:700;
        color:{TEXT};
        """)

        self.subtitle_label = QLabel(subtitle)

        self.subtitle_label.setStyleSheet(f"""
        font-size:{SMALL_SIZE}pt;
        color:{TEXT_MUTED};
        """)

        layout.addWidget(self.title_label)
        layout.addWidget(self.status_indicator)
        layout.addStretch()
        layout.addWidget(self.value_label)
        layout.addWidget(self.subtitle_label)

    # --------------------------------------------------

    def enterEvent(self, event):

        self.animation.stop()

        self.animation.setStartValue(
            self.shadow.blurRadius()
        )

        self.animation.setEndValue(30)

        self.animation.start()

        self.setStyleSheet(f"""
        QFrame#DashboardCard{{
            background:#263244;
            border:1px solid {PRIMARY};
            border-radius:16px;
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

        self.animation.setEndValue(18)

        self.animation.start()

        self.setStyleSheet(f"""
        QFrame#DashboardCard{{
            background:#1F2937;
            border:1px solid #334155;
            border-radius:16px;
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

    def set_subtitle(self, text: str):

        self.subtitle_label.setText(str(text))

    def set_status_color(self, color: str):

        self._accent = color

        self.status_indicator.setStyleSheet(f"""
        background:{color};
        border-radius:2px;
        """)

        self.value_label.setStyleSheet(f"""
        font-size:30pt;
        font-weight:700;
        color:{color};
        """)

    def set_normal(self):

        self.set_status_color(SUCCESS)

    def set_warning(self):

        self.set_status_color("#F59E0B")

    def set_error(self):

        self.set_status_color("#EF4444")