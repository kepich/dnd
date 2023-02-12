from PyQt6.QtWidgets import QMainWindow, QTabWidget

from character.spells.MySpellsWidget import MySpellsWidget
from character.spells.SpellBookWindow import SpellBookWindow


class MagicWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Magic")

        self.mySpells = []

        self.setMinimumWidth(1250)
        self.setMinimumHeight(700)

        self.mySpells = MySpellsWidget(self)

        self.spellBook = SpellBookWindow(self)
        self.spellBook.addRemoveSignal.connect(self.mySpells.addSpellToMyBook)

        centralWidget = QTabWidget()

        centralWidget.addTab(self.mySpells, "My spells")
        centralWidget.addTab(self.spellBook, "Spell book")

        self.setCentralWidget(centralWidget)

    def getData(self):
        return self.mySpells.getData()

    def setData(self, data: dict):
        self.mySpells.setData(data)
