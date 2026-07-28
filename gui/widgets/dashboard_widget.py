import psutil
import time

from datetime import datetime
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QGridLayout,
    QVBoxLayout,
    QWidget,
)

from gui.theme import (
    SPACING,
    CARD_PADDING,
    scale,
)

from gui.widgets.dashboard.welcome_banner import WelcomeBanner
from gui.widgets.dashboard.quick_actions import QuickActions
from gui.widgets.dashboard.status_strip import StatusStrip
from gui.widgets.dashboard.conversation_panel import ConversationPanel
from gui.widgets.dashboard.activity_panel import ActivityPanel


class DashboardWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self._build_ui()

        self.start_time = time.time()

        self.timer = QTimer(self)

        self.timer.timeout.connect(
            self.refresh_dashboard
        )

        self.timer.start(1000)

        self.refresh_dashboard()

    def refresh_dashboard(self) -> None:

        elapsed = int(
            time.time() - self.start_time
        )

        hours, remainder = divmod(elapsed, 3600)

        minutes, seconds = divmod(
            remainder,
            60,
        )

        uptime = (
            f"{hours:02}:"
            f"{minutes:02}:"
            f"{seconds:02}"
        )

        self.set_uptime(uptime)

    def _get_uptime(self) -> str:

        seconds = int(time.time() - self.start_time)

        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def set_assistant_state(
        self,
        state: str,
    ) -> None:

        self.status_strip.set_voice(state)

        self.add_activity(
            f"Assistant: {state}"
        )

    def add_activity(
        self,
        text: str,
    ) -> None:

        timestamp = datetime.now().strftime("%H:%M:%S")

        self.activity_panel.add_activity(
            f"{timestamp}  {text}"
        )

    # --------------------------------------------------
    # UI
    # --------------------------------------------------

    def _build_ui(self):

        self.root = QVBoxLayout(self)

        self.root.setContentsMargins(
            scale(CARD_PADDING),
            scale(CARD_PADDING),
            scale(CARD_PADDING),
            scale(CARD_PADDING),
        )

        self.root.setSpacing(
            scale(SPACING)
        )

        # ------------------------------------------
        # Welcome Banner
        # ------------------------------------------

        self.banner = WelcomeBanner()

        self.root.addWidget(
            self.banner
        )

        # ------------------------------------------
        # Quick Actions
        # ------------------------------------------

        self.quick_actions = QuickActions()

        self.root.addWidget(
            self.quick_actions
        )

        # ------------------------------------------
        # Assistant Status
        # ------------------------------------------

        self.status_strip = StatusStrip()

        self.root.addWidget(
            self.status_strip
        )

        # ------------------------------------------
        # Bottom Panels
        # ------------------------------------------

        self.bottom_layout = QGridLayout()

        self.bottom_layout.setHorizontalSpacing(
            scale(SPACING)
        )

        self.bottom_layout.setVerticalSpacing(
            scale(SPACING)
        )

        self.bottom_layout.setColumnStretch(
            0,
            1,
        )

        self.bottom_layout.setColumnStretch(
            1,
            1,
        )

        self.conversation_panel = ConversationPanel()

        self.activity_panel = ActivityPanel()

        self.bottom_layout.addWidget(
            self.conversation_panel,
            0,
            0,
        )

        self.bottom_layout.addWidget(
            self.activity_panel,
            0,
            1,
        )

        self.root.addLayout(
            self.bottom_layout
        )

        self.root.addStretch()

        # ------------------------------------------
        # Default Values
        # ------------------------------------------

        self.banner.set_user("Vasanth")

        self.banner.set_model("qwen2.5")

        self.status_strip.set_model("qwen2.5")

        self.status_strip.set_voice("Ready")

        self.status_strip.set_memory("Active")

        self.status_strip.set_cpu("-- %")

        self.status_strip.set_ram("-- %")

        self.status_strip.set_disk("-- %")

        self.load_demo_data()


    def refresh_stats(self) -> None:

        cpu = psutil.cpu_percent()

        ram = psutil.virtual_memory().percent

        disk = psutil.disk_usage("/").percent

        self.set_cpu(f"{cpu:.0f}%")

        self.set_ram(f"{ram:.0f}%")

        self.set_disk(f"{disk:.0f}%")
        # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def set_user(
        self,
        name: str,
    ) -> None:

        self.banner.set_user(name)

    def set_model(
        self,
        model: str,
    ) -> None:

        self.banner.set_model(model)
        self.status_strip.set_model(model)

    def set_voice(
        self,
        status: str,
        description: str = "",
    ) -> None:

        self.status_strip.set_voice(status)

        if description:
            self.add_activity(
                f"Voice: {description}"
            )

    def set_memory(
        self,
        status: str,
        description: str = "",
    ) -> None:

        self.status_strip.set_memory(status)

        if description:
            self.add_activity(
                f"Memory: {description}"
            )

    def set_cpu(
        self,
        value: str,
    ) -> None:

        self.status_strip.set_cpu(value)

    def set_ram(
        self,
        value: str,
    ) -> None:

        self.status_strip.set_ram(value)

    def set_disk(
        self,
        value: str,
    ) -> None:

        self.status_strip.set_disk(value)

    def set_ai_status(
        self,
        status: str,
    ) -> None:

        self.status_strip.set_ai_status(status)


    def set_uptime(
        self,
        value: str,
    ) -> None:

        self.status_strip.set_uptime(value)


    def set_conversations(
        self,
        count: int,
    ) -> None:

        self.status_strip.set_conversations(str(count))

    def set_recent_conversations(
        self,
        conversations: list[str],
    ) -> None:

        self.conversation_panel.set_conversations(
            conversations
        )

    def clear_activity(
        self,
    ) -> None:

        self.activity_panel.clear()

    def enable_actions(
        self,
        enabled: bool = True,
    ) -> None:

        self.quick_actions.set_enabled(
            enabled
        )

    # --------------------------------------------------
    # Convenience Helpers
    # --------------------------------------------------

    def reset_dashboard(self) -> None:

        self.clear_activity()

        self.set_recent_conversations([])

        self.set_voice("Ready")

        self.set_memory("Active")

        self.set_cpu("-- %")

        self.set_ram("-- %")

        self.set_disk("-- %")

        self.set_ai_status("Ready")
        self.set_uptime("00:00:00")
        self.set_conversations(0)

    def load_demo_data(self) -> None:

        self.set_recent_conversations(
            [
                "Welcome to Cipher",
                "Python Practice",
                "Linux Commands",
                "Dashboard Redesign",
            ]
        )

        self.add_activity(
            "Cipher Started"
        )

        self.add_activity(
            "AI Model Loaded"
        )

        self.add_activity(
            "Voice Ready"
        )

        self.set_ai_status("Ready")
        self.set_uptime("00:15:42")
        self.set_conversations(4)