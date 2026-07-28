from gui.pages.page_constants import PAGE_DASHBOARD


from dataclasses import dataclass


@dataclass
class PageState:
    """
    Stores the current page state.
    """

    current: str = PAGE_DASHBOARD
    previous: str | None = None

    # --------------------------------------------------

    def change(
        self, 
        page: str,
    ) -> None:

        if page == self.current:
            return

        self.previous = self.current
        self.current = page

    # --------------------------------------------------

    def reset(
        self,
    ) -> None:

        self.current = PAGE_DASHBOARD
        self.previous = None