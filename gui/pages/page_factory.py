from PyQt6.QtWidgets import QWidget

from gui.widgets.dashboard_widget import DashboardWidget
from gui.widgets.chat_panel import ChatPanel

from gui.pages.about_page import AboutPage
from gui.pages.export_chat_page import ExportChatPage
from gui.pages.files_page import FilesPage
from gui.pages.home_page import HomePage
from gui.pages.loading_page import LoadingPage
from gui.pages.memory_page import MemoryPage
from gui.pages.page_not_found import PageNotFound
from gui.pages.plugin_manager_page import PluginManagerPage
from gui.pages.settings_page import SettingsPage
from gui.pages.system_page import SystemPage
from gui.pages.voice_page import VoicePage


def create_pages() -> dict[str, QWidget]:
    """
    Create and return all application pages.
    """

    from gui.pages.page_constants import (
        PAGE_LOADING,
        PAGE_HOME,
        PAGE_DASHBOARD,
        PAGE_CHAT,
        PAGE_MEMORY,
        PAGE_FILES,
        PAGE_SYSTEM,
        PAGE_SETTINGS,
        PAGE_PLUGINS,
        PAGE_VOICE,
        PAGE_EXPORT,
        PAGE_ABOUT,
        PAGE_NOT_FOUND,
    )

    return {
        PAGE_LOADING: LoadingPage(),
        PAGE_HOME: HomePage(),
        PAGE_DASHBOARD: DashboardWidget(),
        PAGE_CHAT: ChatPanel(),
        PAGE_MEMORY: MemoryPage(),
        PAGE_FILES: FilesPage(),
        PAGE_SYSTEM: SystemPage(),
        PAGE_SETTINGS: SettingsPage(),
        PAGE_PLUGINS: PluginManagerPage(),
        PAGE_VOICE: VoicePage(),
        PAGE_EXPORT: ExportChatPage(),
        PAGE_ABOUT: AboutPage(),
        PAGE_NOT_FOUND: PageNotFound(),
    }