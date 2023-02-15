from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QGridLayout

from character.ButtonsWidget import ButtonsWidget


class BasicStatsWidget(QWidget):
    def __init__(self, buttons: ButtonsWidget, parent=None):
        super().__init__(parent)

        self.grid = QGridLayout()
        self.grid.setVerticalSpacing(0)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.grid)

        self.armorClass = QLineEdit()
        self.armorClass.setValidator(QIntValidator(0, 50, self))
        self.armorClass.setFixedWidth(45)

        self.initiative = QLineEdit()
        self.initiative.setValidator(QIntValidator(-30, 30, self))
        self.initiative.setFixedWidth(45)

        self.speed = QLineEdit()
        self.speed.setValidator(QIntValidator(0, 300, self))
        self.speed.setFixedWidth(45)

        self.hp = QLineEdit()
        self.hp.setValidator(QIntValidator(0, 1000, self))
        self.hp.setFixedWidth(45)

        self.maxHp = QLineEdit()
        self.maxHp.setValidator(QIntValidator(0, 1000, self))
        self.maxHp.setFixedWidth(45)

        self.tempHp = QLineEdit()
        self.tempHp.setValidator(QIntValidator(0, 1000, self))
        self.tempHp.setFixedWidth(45)

        self.hpDice = QLineEdit()
        self.hpDice.setFixedWidth(45)

        self.profBonus = QLabel()

        self.grid.addWidget(QLabel("PB:"), 0, 0, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.profBonus, 0, 1, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(QLabel("AC:"), 0, 2, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.armorClass, 0, 3, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(QLabel("HP:"), 1, 0, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.hp, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(QLabel("Max HP:"), 1, 2, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.maxHp, 1, 3, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(QLabel("Temp HP:"), 2, 0, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.tempHp, 2, 1, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(QLabel("HP Dice:"), 2, 2, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.hpDice, 2, 3, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(QLabel("Init:"), 3, 0, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.initiative, 3, 1, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(QLabel("Speed:"), 3, 2, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.speed, 3, 3, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(buttons, 4, 0, 1, 4, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)

    def updateProficiencyBonus(self, profBonus: int):
        self.profBonus.setText(str(profBonus))

    def getData(self):
        return {
            "armorClass": self.armorClass.text(),
            "initiative": self.initiative.text(),
            "speed": self.speed.text(),
            "hp": self.hp.text(),
            "maxHp": self.maxHp.text(),
            "tempHp": self.tempHp.text(),
            "hpDice": self.hpDice.text(),
            "profBonus": self.profBonus.text()
        }

    def setData(self, data: dict):
        self.armorClass.setText(data["armorClass"])
        self.initiative.setText(data["initiative"])
        self.speed.setText(data["speed"])
        self.hp.setText(data["hp"])
        self.tempHp.setText(data["tempHp"])
        self.maxHp.setText(data["maxHp"])
        self.hpDice.setText(data["hpDice"])
        self.profBonus.setText(data["profBonus"])
