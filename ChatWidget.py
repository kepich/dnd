from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget


class ChatWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.vLayout = QVBoxLayout()
        self.chat = QListWidget()
        self.chat.setWordWrap(True)
        self.chat.setFixedHeight(300)
        self.vLayout.addWidget(self.chat)
        self.setLayout(self.vLayout)

    def addChatMessage(self, fromUser, msg):
        self.chat.addItem(f"{fromUser}> {msg}")

    def clearChat(self):
        self.chat.clear()