from collections import deque


class PageHistory:
    """
    Maintains page navigation history.
    """

    def __init__(
        self, 
        max_size: int = 50,
    ) -> None:

        self._history = deque(maxlen=max_size)

    # --------------------------------------------------

    def push(
        self, 
        page: str,
    ) -> None:

        if not page:
            return

        if self._history and self._history[-1] == page:
            return

        self._history.append(page)

    # --------------------------------------------------

    def back(
        self,
    ) -> str | None:

        if len(self._history) <= 1:
            return None

        self._history.pop()

        return self._history[-1]

    # --------------------------------------------------

    def current(
        self,
    ) -> str | None:

        if not self._history:
            return None

        return self._history[-1]

    # --------------------------------------------------

    def clear(
        self,
    ) -> None:

        self._history.clear()

    # --------------------------------------------------

    def items(
        self,
    ) -> list[str]:

        return list(self._history)