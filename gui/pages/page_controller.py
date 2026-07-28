from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import (
    QStackedWidget,
    QWidget,
)


class PageController(QObject):
    """
    Controls page navigation for the stacked widget.
    """

    def __init__(
        self, 
        stack: QStackedWidget,
    ) -> None:
        super().__init__()

        self._stack = stack
        self._pages = {}

    # --------------------------------------------------

    def add_page(
        self, 
        name: str, 
        widget: QWidget,
    ) -> None:

        if name in self._pages:
            return

        self._pages[name] = widget
        self._stack.addWidget(widget)

    # --------------------------------------------------

    def show_page(
        self, 
        name: str,
    ) -> bool:

        widget = self._pages.get(name)

        if widget is None:
            return False

        self._stack.setCurrentWidget(widget)
        return True

    # --------------------------------------------------

    def current_page(
        self,
    ) -> str | None:

        widget = self._stack.currentWidget()

        for name, page in self._pages.items():
            if page is widget:
                return name

        return None

    # --------------------------------------------------

    def page(
        self, 
        name: str,
    ) -> QWidget | None:

        return self._pages.get(name)

    # --------------------------------------------------

    def pages(
        self,
    ) -> dict[str, QWidget]:

        return self._pages.copy()