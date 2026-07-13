from dataclasses import dataclass


@dataclass
class PageState:
    """
    Stores the current page state.
    """

    current: str = "dashboard"
    previous: str | None = None

    # --------------------------------------------------

    def change(self, page: str):

        if page == self.current:
            return

        self.previous = self.current
        self.current = page

    # --------------------------------------------------

    def reset(self):

        self.current = "dashboard"
        self.previous = None