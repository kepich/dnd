from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QCheckBox, QGridLayout

from character.ButtonsWidget import ButtonsWidget


class BasicStatsWidget(QWidget):
    def __init__(self, buttons: ButtonsWidget, parent=None):
        super().__init__(parent)

        self.grid = QGridLayout()
        self.grid.setVerticalSpacing(0)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.grid)

        self.armorClass = QLineEdit()
        self.armorClass.setFixedWidth(45)

        self.initiative = QLineEdit()
        self.initiative.setFixedWidth(45)

        self.speed = QLineEdit()
        self.speed.setFixedWidth(45)

        self.hp = QLineEdit()
        self.hp.setFixedWidth(45)

        self.hpDice = QLineEdit()
        self.hpDice.setFixedWidth(45)

        self.profBonus = QLineEdit()
        self.profBonus.setFixedWidth(45)

        self.grid.addWidget(QLabel("PB:"), 0, 0, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.profBonus, 0, 1, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(QLabel("AC:"), 0, 2, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.armorClass, 0, 3, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(QLabel("HP:"), 1, 0, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.hp, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(QLabel("HP Dice:"), 1, 2, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.hpDice, 1, 3, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(QLabel("Init:"), 2, 0, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.initiative, 2, 1, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(QLabel("Speed:"), 2, 2, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.speed, 2, 3, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(buttons, 3, 0, 1, 4, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)