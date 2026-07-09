from __future__ import annotations

from PyQt6.QtCore import QObject, QTimer
from PyQt6.QtWidgets import QAbstractScrollArea, QScrollArea


class ChatScrollManager(QObject):
    """
    Utility class that manages chat scrolling behavior.

    Features
    --------
    • Smooth auto-scroll to newest message
    • Detect whether user is reading older messages
    • Preserve user's scroll position
    • Resume auto-scroll when user returns to bottom
    """

    BOTTOM_THRESHOLD = 40

    def __init__(self, scroll_area: QScrollArea):
        super().__init__(scroll_area)

        self.scroll_area = scroll_area
        self.scrollbar = scroll_area.verticalScrollBar()

        self._auto_scroll = True

        self.scrollbar.valueChanged.connect(self._on_scroll)

    # ------------------------------------------------------------------

    @property
    def auto_scroll_enabled(self) -> bool:
        return self._auto_scroll

    # ------------------------------------------------------------------

    def scroll_to_bottom(self):
        """
        Scroll immediately.
        """

        self.scrollbar.setValue(self.scrollbar.maximum())

    # ------------------------------------------------------------------

    def scroll_to_bottom_later(self, delay: int = 0):
        """
        Scroll after layouts finish updating.
        """

        if not self._auto_scroll:
            return

        QTimer.singleShot(delay, self.scroll_to_bottom)

    # ------------------------------------------------------------------

    def save_position(self) -> int:
        return self.scrollbar.value()

    # ------------------------------------------------------------------

    def restore_position(self, value: int):
        self.scrollbar.setValue(value)

    # ------------------------------------------------------------------

    def is_at_bottom(self) -> bool:
        return (
            self.scrollbar.maximum()
            - self.scrollbar.value()
            <= self.BOTTOM_THRESHOLD
        )

    # ------------------------------------------------------------------

    def enable_auto_scroll(self):
        self._auto_scroll = True

    def disable_auto_scroll(self):
        self._auto_scroll = False

    # ------------------------------------------------------------------

    def _on_scroll(self, value: int):
        del value

        if self.is_at_bottom():
            self._auto_scroll = True
        else:
            self._auto_scroll = False

    # ------------------------------------------------------------------

    def attach(self, area: QAbstractScrollArea):
        """
        Optional helper if scroll area changes.
        """

        if area is self.scroll_area:
            return

        try:
            self.scrollbar.valueChanged.disconnect(self._on_scroll)
        except Exception:
            pass

        self.scroll_area = area
        self.scrollbar = area.verticalScrollBar()

        self.scrollbar.valueChanged.connect(self._on_scroll)