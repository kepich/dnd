import json

from PyQt6.QtWidgets import QWidget, QScrollArea, QPushButton, QVBoxLayout, QGridLayout, QComboBox

from character.CastWidget import CastWidget

profs = {

}

class SpellBook(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.casts = json.load(open('resources/skills.json', encoding="utf8"))

        self.profession = QComboBox()
        self.profession.addItems(self.casts.keys())
        self.profession.currentTextChanged.connect(self.search)

        self.tier = QComboBox()
        tiers = ["Трюк"]
        tiers.extend([f"{i} круг" for i in range(1, 10)])
        self.tier.addItems(tiers)
        self.tier.currentTextChanged.connect(self.search)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.page = 0
        self.prevPage = QPushButton("Prev page")
        self.nextPage = QPushButton("Next page")

        grid = QGridLayout()

        grid.addWidget(self.profession, 0, 0)
        grid.addWidget(self.tier, 0, 1)
        grid.addWidget(self.scrollArea, 1, 0, 1, 2)
        grid.addWidget(self.prevPage, 2, 0)
        grid.addWidget(self.nextPage, 2, 1)

        self.setLayout(grid)
        self.search()

    def search(self):
        # init needed widgets on page
        prof = self.profession.currentText()
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
            grid.addWidget(castWidget, i // lineSize, i % lineSize)
            i += 1
            print(castWidget.geometry())

        self.scrollArea.setWidget(widget)
