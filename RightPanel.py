from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QHBoxLayout, QTextEdit


class RightPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setFixedWidth(300)

        self.addElements()
        self.vertical_layout.addStretch(1)
        self.addChat()

        self.setLayout(self.vertical_layout)

    def addElements(self):
        firstRow = QHBoxLayout()
        self.addCheckBoxes(firstRow)
        self.vertical_layout.addLayout(firstRow)

    def addCheckBoxes(self, layout):
        self.showGridCheckBox = QCheckBox("Grid")
        self.showGridCheckBox.setChecked(True)
        self.showGridCheckBox.stateChanged.connect(
            lambda: self.parent().canvas.setGridVisibility(self.showGridCheckBox.isChecked()))
        layout.addWidget(self.showGridCheckBox)

        self.darknessCheckBox = QCheckBox("Darkness")
        layout.addWidget(self.darknessCheckBox)

    def addChat(self):
        self.chat = QTextEdit()
        self.chat.setReadOnly(True)
        self.chatMessages = []
        self.chat.setFixedHeight(300)
        self.vertical_layout.addWidget(self.chat)

    def addChatMessage(self, fromUser, msg):
        self.chatMessages.append(f"{fromUser}> {msg}<br>")
        self.chat.setHtml(''.join(self.chatMessages))

    def clearChat(self):
        self.chatMessages.clear()
        self.chat.setHtml("")
