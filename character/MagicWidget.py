import json

from PyQt6 import QtGui
from PyQt6.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QLabel, QScrollArea, QHBoxLayout, QPushButton


class MagicWidget(QWidget):
    def __init__(self, parent=None, name: str = ""):
        super().__init__(parent)

        self.data = ""

        f = open('resources/skills.json', encoding="utf8")
        casts = json.load(f)

        self.textEdit = QTextEdit()
        self.textEdit.setText(str(casts))

        self.scrollAreaLeft = QScrollArea()
        vLayoutL = QVBoxLayout()
        self.scrollAreaLeft.setLayout(vLayoutL)

        self.scrollAreaRight = QScrollArea()
        vLayoutR = QVBoxLayout()
        self.spellBookButton = QPushButton("Spell book")
        vLayoutR.addWidget(self.spellBookButton)
        vLayoutR.addWidget(self.textEdit)
        self.scrollAreaRight.setLayout(vLayoutR)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(name))
        hLayout = QHBoxLayout()
        hLayout.addWidget(self.scrollAreaLeft, stretch=2)
        hLayout.addWidget(self.scrollAreaRight, stretch=1)
        layout.addLayout(hLayout)
        self.setLayout(layout)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.data = self.textEdit.toPlainText()
        a0.accept()

    def getData(self):
        return {
            "data": self.data
        }

    def setData(self, data: dict):
        self.data = data["data"]
        self.textEdit.setText(data["data"])
