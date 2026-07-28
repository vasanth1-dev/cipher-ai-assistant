 from gui.pages.page_constants import PAGE_DASHBOARD

from PyQt6.QtCore import QObject, pyqtSignal


class PageRouter(QObject):
    """
    Central page navigation router for Cipher v2.
    """

    pageChanged = pyqtSignal(str)

     def __init__(
       self,
    ) -> None:
        super().__init__()

        self._current_page = PAGE_DASHBOARD

    # --------------------------------------------------

    @property
    def current_page(self) -> str:
        return self._current_page

    # --------------------------------------------------

    def navigate(
        self, 
        page: str,
    ) -> None:

        if not page:
            return

        if page == self._current_page:
            return

        self._current_page = page

        self.pageChanged.emit(page)

    # --------------------------------------------------

    def reset(
        self,
    ) -> None:

        self.navigate(PAGE_DASHBOARD)