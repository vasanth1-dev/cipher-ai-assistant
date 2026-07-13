from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QTextEdit,
)

from gui.theme import (
    BACKGROUND,
    SURFACE,
    BORDER,
    PRIMARY,
    PRIMARY_HOVER,
    TEXT,
    TEXT_MUTED,
)


class PluginManagerPage(QWidget):

    enableClicked = pyqtSignal(str)
    disableClicked = pyqtSignal(str)
    reloadClicked = pyqtSignal(str)
    uninstallClicked = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._build_ui()

    def _build_ui(self):

        self.setStyleSheet(f"""
        QWidget{{
            background:{BACKGROUND};
            color:{TEXT};
        }}

        QLineEdit,
        QListWidget,
        QTextEdit{{
            background:{SURFACE};
            color:{TEXT};
            border:1px solid {BORDER};
            border-radius:10px;
        }}

        QLineEdit{{
            padding:10px;
        }}

        QListWidget::item{{
            padding:10px;
        }}

        QPushButton{{
            background:{PRIMARY};
            color:white;
            border:none;
            border-radius:8px;
            padding:10px 18px;
            font-weight:bold;
        }}

        QPushButton:hover{{
            background:{PRIMARY_HOVER};
        }}
        """)

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(15)

        title = QLabel("🔌 Plugin Manager")
        title.setStyleSheet("""
        font-size:24px;
        font-weight:bold;
        """)

        subtitle = QLabel("Manage Cipher plugins")
        subtitle.setStyleSheet(f"""
        color:{TEXT_MUTED};
        font-size:10pt;
        """)

        root.addWidget(title)
        root.addWidget(subtitle)

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search plugins...")
        self.search.textChanged.connect(self._filter_plugins)

        root.addWidget(self.search)

        content = QHBoxLayout()

        self.plugin_list = QListWidget()
        self.plugin_list.currentItemChanged.connect(
            self._plugin_changed
        )

        right = QVBoxLayout()

        self.info = QTextEdit()
        self.info.setReadOnly(True)

        buttons = QHBoxLayout()

        self.enable_button = QPushButton("Enable")
        self.disable_button = QPushButton("Disable")
        self.reload_button = QPushButton("Reload")
        self.uninstall_button = QPushButton("Uninstall")

        self.enable_button.clicked.connect(self._enable)
        self.disable_button.clicked.connect(self._disable)
        self.reload_button.clicked.connect(self._reload)
        self.uninstall_button.clicked.connect(self._uninstall)

        buttons.addWidget(self.enable_button)
        buttons.addWidget(self.disable_button)
        buttons.addWidget(self.reload_button)
        buttons.addWidget(self.uninstall_button)

        right.addWidget(self.info, 1)
        right.addLayout(buttons)

        content.addWidget(self.plugin_list, 1)
        content.addLayout(right, 2)

        root.addLayout(content)

    # --------------------------------------------------

    def set_plugins(self, plugins):

        self.plugin_list.clear()

        for plugin in plugins:

            if isinstance(plugin, dict):

                name = plugin.get("name", "Unknown")
                enabled = plugin.get("enabled", False)

                status = "🟢" if enabled else "⚪"

                item = QListWidgetItem(f"{status} {name}")
                item.setData(Qt.ItemDataRole.UserRole, plugin)

            else:

                item = QListWidgetItem(str(plugin))
                item.setData(
                    Qt.ItemDataRole.UserRole,
                    {"name": str(plugin), "enabled": False},
                )

            self.plugin_list.addItem(item)

    # --------------------------------------------------

    def _plugin_changed(self, current, previous):

        if current is None:
            self.info.clear()
            return

        plugin = current.data(Qt.ItemDataRole.UserRole)

        self.info.setPlainText(
            f"Name : {plugin.get('name','Unknown')}\n"
            f"Enabled : {plugin.get('enabled', False)}"
        )

    def _selected_name(self):

        item = self.plugin_list.currentItem()

        if item is None:
            return None

        return item.data(
            Qt.ItemDataRole.UserRole
        ).get("name")

    def _enable(self):

        name = self._selected_name()

        if name:
            self.enableClicked.emit(name)

    def _disable(self):

        name = self._selected_name()

        if name:
            self.disableClicked.emit(name)

    def _reload(self):

        name = self._selected_name()

        if name:
            self.reloadClicked.emit(name)

    def _uninstall(self):

        name = self._selected_name()

        if name:
            self.uninstallClicked.emit(name)

    def _filter_plugins(self, text):

        text = text.lower()

        for row in range(self.plugin_list.count()):

            item = self.plugin_list.item(row)

            item.setHidden(
                text not in item.text().lower()
            )