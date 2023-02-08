from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel

from character.StateWidget import StateWidget


class StatblockWidget(QWidget):
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
