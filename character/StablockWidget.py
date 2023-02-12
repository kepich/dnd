from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel

from character.stats.StatsWidget import StateWidget


class StatBlockWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.grid = QGridLayout()
        self.grid.setVerticalSpacing(0)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.grid)

        self.grid.addWidget(QLabel("Val"), 0, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        self.grid.addWidget(QLabel("Mod"), 0, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        self.grid.addWidget(QLabel("S/Th"), 0, 3, alignment=Qt.AlignmentFlag.AlignCenter)

        self.strengthWidget = StateWidget("STR", self.grid, 1)
        self.dexterityWidget = StateWidget("DEX", self.grid, 2)
        self.constitutionWidget = StateWidget("CONST", self.grid, 3)
        self.intelligenceWidget = StateWidget("INT", self.grid, 4)
        self.wisdomWidget = StateWidget("WSD", self.grid, 5)
        self.charismaWidget = StateWidget("CHR", self.grid, 6)

    def updateProficiencyBonus(self, profBonus: int):
        self.strengthWidget.updateProficiencyBonus(profBonus)
        self.dexterityWidget.updateProficiencyBonus(profBonus)
        self.constitutionWidget.updateProficiencyBonus(profBonus)
        self.intelligenceWidget.updateProficiencyBonus(profBonus)
        self.wisdomWidget.updateProficiencyBonus(profBonus)
        self.charismaWidget.updateProficiencyBonus(profBonus)

    def getData(self):
        return {
            "strength": self.strengthWidget.getData(),
            "dexterity": self.dexterityWidget.getData(),
            "constitution": self.constitutionWidget.getData(),
            "intelligence": self.intelligenceWidget.getData(),
            "wisdom": self.wisdomWidget.getData(),
            "charisma": self.charismaWidget.getData()
        }

    def setData(self, data: dict):
        self.strengthWidget.setData(data["strength"])
        self.dexterityWidget.setData(data["dexterity"])
        self.constitutionWidget.setData(data["constitution"])
        self.intelligenceWidget.setData(data["intelligence"])
        self.wisdomWidget.setData(data["wisdom"])
        self.charismaWidget.setData(data["charisma"])
