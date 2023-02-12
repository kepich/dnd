from PyQt6 import QtGui
from PyQt6.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QLabel, QScrollArea, QHBoxLayout, QPushButton, QMainWindow

from character.spells.SpellWidget import CastWidget
from character.spells.SpellBookWindow import SpellBookWindow


class MagicWindow(QMainWindow):
    def __init__(self, parent=None, name: str = ""):
        super().__init__(parent)
        hLayout = QHBoxLayout()
        self.mySpells = []

        self.setMinimumWidth(1250)
        self.setMinimumHeight(700)

        self.scrollAreaLeft = QScrollArea()
        self.scrollAreaWidget = QWidget()
        self.scrollAreaLeft.setWidget(self.scrollAreaWidget)
        hLayout.addWidget(self.scrollAreaLeft, stretch=2)

        self.scrollAreaRight = QScrollArea()
        vLayoutR = QVBoxLayout()
        self.spellBookButton = QPushButton("Spell book")
        self.spellBook = SpellBookWindow(self)
        self.spellBook.addRemoveSignal.connect(self.addSpellToMyBook)
        self.spellBookButton.pressed.connect(lambda: self.spellBook.show())
        vLayoutR.addWidget(self.spellBookButton)

        self.data = ""
        self.otherMagic = QTextEdit()
        vLayoutR.addWidget(self.otherMagic)
        self.scrollAreaRight.setLayout(vLayoutR)
        hLayout.addWidget(self.scrollAreaRight, stretch=1)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(name))

        layout.addLayout(hLayout)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def addSpellToMyBook(self, cast):
        self.mySpells.append(cast)
        self.redrawSpells()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.data = self.otherMagic.toPlainText()
        a0.accept()

    def getData(self):
        return {
            "data": self.data,
            "spells": self.mySpells
        }

    def setData(self, data: dict):
        self.data = data["data"]
        self.mySpells = data["spells"]
        self.otherMagic.setText(data["data"])
        self.redrawSpells()

    def redrawSpells(self):
        vLayout = QVBoxLayout()
        for cast in self.mySpells:
            castWidget = CastWidget(cast, isAdded=True)
            castWidget.removeSignal.connect(self.removeSpell)
            vLayout.addWidget(castWidget)
        self.scrollAreaWidget = QWidget()
        self.scrollAreaWidget.setLayout(vLayout)
        self.scrollAreaLeft.setWidget(self.scrollAreaWidget)

    def removeSpell(self, cast):
        self.mySpells.remove(cast)
        self.redrawSpells()
