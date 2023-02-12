from PyQt6 import QtGui
from PyQt6.QtGui import QWindow
from PyQt6.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QLabel, QMainWindow


class NotebookWindow(QMainWindow):
    def __init__(self, parent=None, name: str = ""):
        super().__init__(parent)

        self.setWindowTitle(name)

        self.data = ""

        self.textEdit = QTextEdit()
        self.textEdit.setFixedWidth(600)
        self.textEdit.setFixedHeight(400)

        self.setCentralWidget(self.textEdit)

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