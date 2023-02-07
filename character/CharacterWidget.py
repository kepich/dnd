from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QGridLayout


class CharacterWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.hLayout = QHBoxLayout()
        self.setLayout(self.hLayout)

        self.miniatureLabel = QLabel("Miniature")
        self.hLayout.addWidget(self.miniatureLabel)

        self.nickname = QLineEdit()
        self.lvl = QLineEdit()

        self.race = QLineEdit()
        self.prof = QLineEdit()

        self.grid1 = QGridLayout()
        self.hLayout.addLayout(self.grid1)
        self.grid1.addWidget(self.nickname, 0, 0)
        self.grid1.addWidget(self.lvl, 0, 1)
        self.grid1.addWidget(self.race, 1, 0)
        self.grid1.addWidget(self.prof, 1, 1)

