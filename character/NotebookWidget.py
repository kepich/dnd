from PyQt6.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QLabel
from PyQt6 import QtGui


class NotebookWidget(QWidget):
    def __init__(self, parent=None, name: str = ""):
        super().__init__(parent)

        self.data = ""

        self.textEdit = QTextEdit()
        self.textEdit.setFixedWidth(600)
        self.textEdit.setFixedHeight(400)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(name))
        layout.addWidget(self.textEdit)
        self.setLayout(layout)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.data = self.textEdit.toPlainText()
        a0.accept()