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

    def __init__(self, stack: QStackedWidget):
        self._stack = stack
        self._pages: Dict[str, QWidget] = {}

    # --------------------------------------------------

    def register_page(
        self,
        name: str,
        page: QWidget,
    ):

        if name in self._pages:
            return

        self._pages[name] = page
        self._stack.addWidget(page)

    # --------------------------------------------------

    def page(self, name: str):

        return self._pages.get(name)

    # --------------------------------------------------

    def show(self, name: str):

        page = self._pages.get(name)

        if page is None:
            return False

        self._stack.setCurrentWidget(page)
        return True

    # --------------------------------------------------

    def contains(self, name: str):

        return name in self._pages

    # --------------------------------------------------

    def names(self):

        return list(self._pages.keys())