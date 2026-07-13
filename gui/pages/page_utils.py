from PyQt6.QtWidgets import QStackedWidget


def page_index(
    stack: QStackedWidget,
    widget,
) -> int:
    """
    Return the index of a page inside a QStackedWidget.
    """

    return stack.indexOf(widget)


def has_page(
    stack: QStackedWidget,
    widget,
) -> bool:
    """
    Check whether a page exists in the stacked widget.
    """

    return stack.indexOf(widget) != -1


def show_page(
    stack: QStackedWidget,
    widget,
) -> bool:
    """
    Display a page if it exists.
    """

    index = stack.indexOf(widget)

    if index == -1:
        return False

    stack.setCurrentIndex(index)
    return True