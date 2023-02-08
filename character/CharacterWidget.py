from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QGridLayout, QCheckBox

from character.StablockWidget import StatblockWidget


class CharacterWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.hLayout = QHBoxLayout()
        self.setLayout(self.hLayout)

        self.miniatureLabel = QLabel("Miniature")
        # self.miniatureLabel.setFixedHeight(70)
        # self.miniatureLabel.setFixedWidth(70)
        # self.hLayout.addWidget(self.miniatureLabel)

        self.nickname = QLineEdit()
        self.nickname.setFixedWidth(100)
        self.nickname.setPlaceholderText("Nickname")
        self.lvl = QLineEdit()
        self.lvl.setFixedWidth(45)
        self.lvl.setPlaceholderText("lvl")
        self.profBonus = QLineEdit()
        self.profBonus.setFixedWidth(45)

        self.race = QLineEdit()
        self.race.setFixedWidth(100)
        self.race.setPlaceholderText("Race")
        self.prof = QLineEdit()
        self.prof.setFixedWidth(100)
        self.prof.setPlaceholderText("Profession")

        self.armorClass = QLineEdit()
        self.armorClass.setFixedWidth(40)

        self.inspiration = QCheckBox("Inspiration")

        self.initiative = QLineEdit()
        self.initiative.setFixedWidth(45)

        self.speed = QLineEdit()
        self.speed.setFixedWidth(45)

        self.hp = QLineEdit()
        self.hp.setFixedWidth(45)

        self.hpDice = QLineEdit()
        self.hpDice.setFixedWidth(45)

        self.grid1 = QGridLayout()
        self.hLayout.addLayout(self.grid1)

        self.grid1.addWidget(self.nickname, 0, 0, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid1.addWidget(self.lvl, 0, 1, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid1.addWidget(self.miniatureLabel, 1, 0, 2, 2, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid1.addWidget(self.race, 3, 0, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid1.addWidget(self.prof, 3, 1, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.grid1.addWidget(QLabel("PB:"), 0, 2, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid1.addWidget(self.profBonus, 0, 3, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid1.addWidget(QLabel("AC:"), 0, 4, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid1.addWidget(self.armorClass, 0, 5, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid1.addWidget(QLabel("HP:"), 1, 2, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid1.addWidget(self.hp, 1, 3, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid1.addWidget(QLabel("HP Dice:"), 1, 4, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid1.addWidget(self.hpDice, 1, 5, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid1.addWidget(QLabel("Init:"), 2, 2, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid1.addWidget(self.initiative, 2, 3, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid1.addWidget(QLabel("Speed:"), 2, 4, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid1.addWidget(self.speed, 2, 5, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.grid1.addWidget(self.inspiration, 3, 2, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)

        self.statblock = StatblockWidget()
        self.hLayout.addWidget(self.statblock, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

