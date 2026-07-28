from typing import Dict

from PyQt6.QtWidgets import QStackedWidget, QWidget


class PageLoader:
    """
    Central page registry for Cipher v2.

    Responsible for:
    - Registering pages
    - Switching pages
    - Looking up pages by name
    """

    def __init__(
        self, 
        stack: QStackedWidget,
    ) -> None:
        self._stack = stack
        self._pages: Dict[str, QWidget] = {}

    # --------------------------------------------------

    def register_page(
        self,
        name: str,
        page: QWidget,
    ) -> None:

        if name in self._pages:
            return

        self._pages[name] = page
        self._stack.addWidget(page)

    # --------------------------------------------------

    def page(
        self, 
        name: str,
    ) -> QWidget | None:

        return self._pages.get(name)

    # --------------------------------------------------

    def show(
        self, 
        name: str,
    ) -> bool:

        page = self._pages.get(name)

        if page is None:
            return False

        self._stack.setCurrentWidget(page)
        return True

    # --------------------------------------------------

    def contains(
        self, 
        name: str,
    ) -> bool:

        return name in self._pages

    # --------------------------------------------------

    def names(
        self,
    ) -> list[str]:

        return list(self._pages.keys())