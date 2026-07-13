from __future__ import annotations

from PyQt6.QtCore import QObject

from services.dashboard_controller import DashboardController
from services.quick_actions_service import QuickActionsService


class DashboardManager(QObject):
    """
    Dashboard Manager

    Coordinates all dashboard-related services.

    Responsibilities
    ----------------
    • Start dashboard services
    • Stop dashboard services
    • Expose quick actions
    """

    def __init__(self, dashboard_widget, parent=None):
        super().__init__(parent)

        self.dashboard = dashboard_widget

        self.controller = DashboardController(
            dashboard_widget,
            self,
        )

        self.actions = QuickActionsService(self)

    # --------------------------------------------------

    def start(self):
        """Start dashboard services."""
        self.controller.start()

    def stop(self):
        """Stop dashboard services."""
        self.controller.stop()

    # --------------------------------------------------
    # Quick Actions
    # --------------------------------------------------

    def open_terminal(self):
        return self.actions.open_terminal()

    def open_browser(self):
        return self.actions.open_browser()

    def open_files(self):
        return self.actions.open_files()

    def open_settings(self):
        return self.actions.open_settings()