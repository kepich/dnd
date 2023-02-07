from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QHBoxLayout, QPushButton, QLineEdit


class ChatWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.vLayout = QVBoxLayout()
        self.chat = QListWidget()
        self.chat.setWordWrap(True)
        self.chat.setFixedHeight(300)
        self.vLayout.addWidget(self.chat)

        self.nickname = None

        self.hLayout = QHBoxLayout()
        self.textBox = QLineEdit()
        self.hLayout.addWidget(self.textBox)
        self.sendButton = QPushButton(">")
        self.sendButton.pressed.connect(self.sendMessageToServer)
        self.hLayout.addWidget(self.sendButton)
        self.vLayout.addLayout(self.hLayout)

        self.setLayout(self.vLayout)

    def sendMessageToServer(self):
        self.parent().parent().canvas.networkProxy.sendMessageToChat(self.textBox.text())
        self.textBox.clear()

    def addChatMessage(self, fromUser, msg):
        self.chat.addItem(f"{fromUser}> {msg}")
        self.chat.scrollToBottom()

    def clearChat(self):
        self.chat.clear()