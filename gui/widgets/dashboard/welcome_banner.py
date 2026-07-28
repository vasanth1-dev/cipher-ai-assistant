from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
)

from gui.theme import (
    SURFACE_LIGHT,
    PRIMARY,
    TEXT,
    TEXT_MUTED,
    CARD_RADIUS,
    scale,
)


class WelcomeBanner(QFrame):
    """
    Dashboard welcome banner.
    """

    def __init__(
        self, 
        parent: QFrame | None = None,
    ) -> None:
        super().__init__(parent)

        self.setObjectName("WelcomeBanner")

        self.setStyleSheet(f"""
        QFrame#WelcomeBanner {{
            background:{SURFACE_LIGHT};
            border:1px solid {PRIMARY};
            border-radius:{CARD_RADIUS}px;
        }}
        """)

        root = QHBoxLayout(self)

        root.setContentsMargins(
            scale(28),
            scale(24),
            scale(28),
            scale(24),
        )
        

        # ---------------- Left ----------------

        left = QVBoxLayout()

        left.setSpacing(
            scale(8)
        )

        self.title = QLabel(
            "👋 Welcome Back"
        )

        self.title.setStyleSheet(f"""
            color:{TEXT};
            font-size:{scale(28)}px;
            font-weight:800;
        """)

        self.subtitle = QLabel(
            "Cipher is ready to help you."
        )

        self.subtitle.setStyleSheet(f"""
            color:{TEXT_MUTED};
            font-size:{scale(12)}pt;
            line-height:1.4;
        """)

        left.addWidget(self.title)
        left.addWidget(self.subtitle)

        # ---------------- Right ----------------

        right = QVBoxLayout()

        right.setSpacing(
            scale(6)
        )

        right.setAlignment(
            Qt.AlignmentFlag.AlignRight |
            Qt.AlignmentFlag.AlignVCenter
        )

        self.status = QLabel("🟢 Online")

        self.status.setStyleSheet(f"""
            color:{PRIMARY};
            font-size:{scale(13)}pt;
            font-weight:800;
        """)

        self.model = QLabel("qwen2.5")

        self.model.setStyleSheet(f"""
            color:{TEXT};
            font-size:{scale(11)}pt;
            font-weight:600;
        """)

        right.addWidget(
            self.status,
            alignment=Qt.AlignmentFlag.AlignRight
        )

        right.addWidget(
            self.model,
            alignment=Qt.AlignmentFlag.AlignRight
        )

        root.addLayout(left, 1)
        root.addLayout(right)

    # -------------------------------------------------

    def set_user(
        self, 
        name: str,
    ) -> None:

        self.title.setText(
            f"👋 Welcome Back, {name}"
        )

    def set_model(
        self, 
        model: str,
    ) -> None:

        self.model.setText(model)

    def set_status(
        self, 
        status: str,
    ) -> None:

        self.status.setText(status)