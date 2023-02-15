from PyQt6.QtWidgets import QDialog, QVBoxLayout, QListWidget, QHBoxLayout, QPushButton, QLineEdit

from utils.SaveManager import SaveManager


class LoadNpcDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Load NPC")
        self.saves = SaveManager().getCharacters()

        self.vLayout = QVBoxLayout()

        self.nameOfNpc = QLineEdit()
        self.nameOfNpc.setPlaceholderText("NPC name")
        self.vLayout.addWidget(self.nameOfNpc)

        self.listBox = QListWidget()
        self.listBox.addItems(self.saves)
        self.listBox.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.vLayout.addWidget(self.listBox)

        self.hLayout = QHBoxLayout()
        self.loadButton = QPushButton("Load")
        self.loadButton.pressed.connect(self.accept)
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.pressed.connect(self.reject)
        self.hLayout.addWidget(self.loadButton)
        self.hLayout.addWidget(self.cancelButton)

        self.vLayout.addLayout(self.hLayout)

        self.setLayout(self.vLayout)

    def getChosenCharacter(self):
        return self.listBox.selectedIndexes()[0].data()
