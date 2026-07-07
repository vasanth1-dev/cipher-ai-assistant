import sys

from PyQt6.QtWidgets import QApplication

from gui.main_window import MainWindow
from gui.chat_widget import ChatManager
from gui.tray import CipherTray
app = QApplication(sys.argv)

window = MainWindow()
tray = CipherTray(window)
chat = ChatManager()

chat.message_received.connect(window.add_message)


def send():

    text = window.input.text().strip()

    if not text:
        return

    chat.user(text)

    # Temporary reply
    chat.cipher(f"I received: {text}")

    window.input.clear()


window.send.clicked.connect(send)

window.show()

sys.exit(app.exec())
