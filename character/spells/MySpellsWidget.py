from PyQt6 import QtGui
from PyQt6.QtWidgets import QWidget, QScrollArea, QHBoxLayout, QVBoxLayout, QTextEdit

from character.spells.SpellWidget import CastWidget


class MySpellsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = ""

        hLayout = QHBoxLayout()
        self.mySpells = []

        self.scrollAreaLeft = QScrollArea()
        self.scrollAreaWidget = QWidget()
        self.scrollAreaLeft.setWidget(self.scrollAreaWidget)
        hLayout.addWidget(self.scrollAreaLeft)

        self.scrollAreaRight = QScrollArea()

        self.otherMagic = QTextEdit()
        vLayoutR = QVBoxLayout()
        vLayoutR.addWidget(self.otherMagic)
        self.scrollAreaRight.setLayout(vLayoutR)
        hLayout.addWidget(self.scrollAreaRight)

        layout = QVBoxLayout()

        layout.addLayout(hLayout)

        self.setLayout(layout)

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

    def addSpellToMyBook(self, cast):
        self.mySpells.append(cast)
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
