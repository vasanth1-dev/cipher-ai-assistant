from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from gui.theme import (
    SURFACE,
    BORDER,
    PRIMARY,
    PRIMARY_HOVER,
    TEXT,
    TEXT_MUTED,
    CARD_RADIUS,
    CARD_PADDING,
    SPACING,
    BUTTON_HEIGHT,
)


class MemoryWidget(QWidget):
    """
    Cipher Memory Center
    """

    def __init__(
        self, 
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self._build_ui()

        self.search.textChanged.connect(
            self.search_memory
        )

        self.clear_button.clicked.connect(
            self.clear_all
        )

        self.update_stats()

    # --------------------------------------------------

    def _build_ui(
        self,
    ) -> None:

        root = QVBoxLayout(self)

        root.setContentsMargins(
            CARD_PADDING,
            CARD_PADDING,
            CARD_PADDING,
            CARD_PADDING,
        )

        root.setSpacing(SPACING)

        # ==========================================
        # Header
        # ==========================================

        header = QFrame()

        header.setStyleSheet(f"""
        QFrame {{
            background:{SURFACE};
            border:1px solid {BORDER};
            border-radius:{CARD_RADIUS}px;
        }}

        QPushButton {{
            background:{PRIMARY};
            color:white;
            border:none;
            border-radius:8px;
            min-height:{BUTTON_HEIGHT}px;
            padding:6px 14px;
        }}

        QPushButton:hover {{
            background:{PRIMARY_HOVER};
        }}
        """)

        header_layout = QHBoxLayout(header)

        title_layout = QVBoxLayout()

        title = QLabel("🧠 Memory Center")

        title.setStyleSheet(f"""
            color:{TEXT};
            font-size:18pt;
            font-weight:700;
        """)

        subtitle = QLabel(
            "Manage Cipher memory"
        )

        subtitle.setStyleSheet(f"""
            color:{TEXT_MUTED};
            font-size:10pt;
        """)

        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)

        header_layout.addLayout(title_layout)

        header_layout.addStretch()

        self.refresh_button = QPushButton("Refresh")

        self.clear_button = QPushButton("Clear")

        header_layout.addWidget(self.refresh_button)
        header_layout.addWidget(self.clear_button)

        root.addWidget(header)

        # ==========================================
        # Search
        # ==========================================

        self.search = QLineEdit()

        self.search.setPlaceholderText(
            "Search memory..."
        )

        root.addWidget(self.search)

        # ==========================================
        # Short Term Memory
        # ==========================================

        short_label = QLabel(
            "Short-Term Memory"
        )

        short_label.setStyleSheet(f"""
            color:{TEXT};
            font-size:13pt;
            font-weight:600;
        """)

        root.addWidget(short_label)

        self.short_memory = QListWidget()

        root.addWidget(
            self.short_memory,
            1,
        )

        # ==========================================
        # Long Term Memory
        # ==========================================

        long_label = QLabel(
            "Long-Term Memory"
        )

        long_label.setStyleSheet(f"""
            color:{TEXT};
            font-size:13pt;
            font-weight:600;
        """)

        root.addWidget(long_label)

        self.long_memory = QListWidget()

        root.addWidget(
            self.long_memory,
            1,
        )

        # ==========================================
        # Stats
        # ==========================================

        self.stats = QLabel(
            "0 Memories"
        )

        self.stats.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.stats.setStyleSheet(f"""
            color:{TEXT_MUTED};
            font-size:10pt;
        """)

        root.addWidget(self.stats)

        # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def add_short_memory(
        self,
        text: str,
    ) -> None:

        self.short_memory.insertItem(
            0,
            text,
        )

        self.update_stats()

    # --------------------------------------------------

    def add_long_memory(
        self,
        text: str,
    ) -> None:

        self.long_memory.insertItem(
            0,
            text,
        )

        self.update_stats()

    # --------------------------------------------------

    def set_short_memory(
        self,
        items: list[str],
    ) -> None:

        self.short_memory.clear()

        self.short_memory.addItems(items)

        self.update_stats()

    # --------------------------------------------------

    def set_long_memory(
        self,
        items: list[str],
    ) -> None:

        self.long_memory.clear()

        self.long_memory.addItems(items)

        self.update_stats()

    # --------------------------------------------------

    def clear_short_memory(
        self,
    ) -> None:

        self.short_memory.clear()

        self.update_stats()

    # --------------------------------------------------

    def clear_long_memory(
        self,
    ) -> None:

        self.long_memory.clear()

        self.update_stats()

    # --------------------------------------------------

    def clear_all(
        self,
    ) -> None:

        self.short_memory.clear()

        self.long_memory.clear()

        self.update_stats()

    # --------------------------------------------------

    def update_stats(
        self,
    ) -> None:

        short_count = self.short_memory.count()

        long_count = self.long_memory.count()

        total = short_count + long_count

        self.stats.setText(
            f"{total} Memories   •   "
            f"{short_count} Short   •   "
            f"{long_count} Long"
        )

    # --------------------------------------------------

    def search_memory(
        self,
        text: str,
    ) -> None:

        text = text.lower()

        for widget in (
            self.short_memory,
            self.long_memory,
        ):

            for index in range(widget.count()):

                item = widget.item(index)

                hidden = (
                    text not in item.text().lower()
                )

                item.setHidden(hidden)

    # --------------------------------------------------

    def load_demo_data(
        self,
    ) -> None:

        self.set_short_memory(
            [
                "User: Hello Cipher",
                "Assistant: Hello Vasanth",
                "Open Firefox",
            ]
        )

        self.set_long_memory(
            [
                "Name : Vasanth",
                "Assistant : Cipher",
                "Model : qwen2.5",
                "Language : English",
            ]
        )

    # --------------------------------------------------

    def export_memory(
        self,
    ) -> dict[str, list[str]]:

        short = []

        long = []

        for i in range(
            self.short_memory.count()
        ):

            short.append(
                self.short_memory.item(i).text()
            )

        for i in range(
            self.long_memory.count()
        ):

            long.append(
                self.long_memory.item(i).text()
            )

        return {
            "short_memory": short,
            "long_memory": long,
        }