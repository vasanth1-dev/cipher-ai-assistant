PAGE_ICONS = {
    "loading": "⏳",
    "home": "🏠",
    "dashboard": "📊",
    "chat": "💬",
    "memory": "🧠",
    "files": "📁",
    "system": "🖥",
    "settings": "⚙",
    "plugins": "🔌",
    "voice": "🎤",
    "export": "📄",
    "about": "ℹ",
    "404": "❌",
}


def icon(page: str) -> str:
    return PAGE_ICONS.get(page, "📄")