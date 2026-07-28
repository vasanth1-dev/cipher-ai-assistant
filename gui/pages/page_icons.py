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

PAGE_ICONS = {
    PAGE_LOADING: "⏳",
    PAGE_HOME: "🏠",
    PAGE_DASHBOARD: "📊",
    PAGE_CHAT: "💬",
    PAGE_MEMORY: "🧠",
    PAGE_FILES: "📁",
    PAGE_SYSTEM: "🖥",
    PAGE_SETTINGS: "⚙",
    PAGE_PLUGINS: "🔌",
    PAGE_VOICE: "🎤",
    PAGE_EXPORT: "📄",
    PAGE_ABOUT: "ℹ",
    PAGE_NOT_FOUND: "❌",
}


def icon(page: str) -> str:
    return PAGE_ICONS.get(page, "📄")