import json

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QScrollArea, QGridLayout, QComboBox, QMainWindow

from character.spells.SpellWidget import CastWidget

profs = {
    'artificer': "изобретатель",
    'bard': "бард",
    'wizard': "волшебник",
    'paladin': "паладин",
    'ranger': "следопыт",
    'cleric': "жрец",
    'sorcerer': "чародей",
    'druid': "друид",
    'warlock': "колдун"
}

profsInverted = {v: k for k, v in profs.items()}


class SpellBookWindow(QMainWindow):
    addRemoveSignal = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.casts = json.load(open('resources/skills.json', encoding="utf8"))

        self.profession = QComboBox()
        self.profession.addItems(list(map(lambda key: profs[key], self.casts.keys())))
        self.profession.currentTextChanged.connect(self.search)

        self.tier = QComboBox()
        tiers = ["Трюк"]
        tiers.extend([f"{i} круг" for i in range(1, 10)])
        self.tier.addItems(tiers)
        self.tier.currentTextChanged.connect(self.search)

        self.scrollArea = QScrollArea()
        self.scrollArea.setMinimumWidth(1250)
        self.scrollArea.setMinimumHeight(700)
        self.scrollArea.horizontalScrollBar().setEnabled(False)

        grid = QGridLayout()

        grid.addWidget(self.profession, 0, 0)
        grid.addWidget(self.tier, 0, 1)
        grid.addWidget(self.scrollArea, 1, 0, 1, 2)

        centralWidget = QWidget()
        centralWidget.setLayout(grid)
        self.setCentralWidget(centralWidget)

        self.search()

    def search(self):
        prof = profsInverted[self.profession.currentText()]
        tier = self.tier.currentText()
        profCasts = self.casts[prof]
        filteredCasts = list(filter(lambda x: x["level"].startswith(tier), profCasts))

        widget = QWidget()
        grid = QGridLayout()
        widget.setLayout(grid)

        i = 0
        lineSize = 2

        for cast in filteredCasts:
            castWidget = CastWidget(cast)
            castWidget.addSignal.connect(self.addRemoveSignal.emit)
            grid.addWidget(castWidget, i // lineSize, i % lineSize)
            i += 1

        self.scrollArea.setWidget(widget)
