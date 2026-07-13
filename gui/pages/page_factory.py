from gui.dashboard_widget import DashboardWidget
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


def create_pages():
    """
    Create and return all application pages.
    """

    return {
        "loading": LoadingPage(),
        "home": HomePage(),
        "dashboard": DashboardWidget(),
        "chat": ChatPanel(),
        "memory": MemoryPage(),
        "files": FilesPage(),
        "system": SystemPage(),
        "settings": SettingsPage(),
        "plugins": PluginManagerPage(),
        "voice": VoicePage(),
        "export": ExportChatPage(),
        "about": AboutPage(),
        "404": PageNotFound(),
    }