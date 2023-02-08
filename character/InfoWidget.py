from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QCheckBox, QGridLayout, QPushButton, QFileDialog

from utils.SaveManager import SaveManager


class InfoWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid = QGridLayout()
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setVerticalSpacing(0)

        self.setLayout(self.grid)

        self.pixmap = None
        self.avatar = QLabel("Avatar")
        self.avatar.setFixedHeight(100)
        self.avatar.setFixedWidth(100)

        self.name = QLineEdit()
        self.name.setFixedWidth(100)
        self.name.setPlaceholderText("Nickname")

        self.lvl = QLineEdit()
        self.lvl.setFixedWidth(45)
        self.lvl.setPlaceholderText("lvl")

        self.race = QLineEdit()
        self.race.setFixedWidth(100)
        self.race.setPlaceholderText("Race")

        self.profession = QLineEdit()
        self.profession.setFixedWidth(100)
        self.profession.setPlaceholderText("Class")

        self.armorClass = QLineEdit()
        self.armorClass.setFixedWidth(45)

        self.inspiration = QCheckBox("Inspiration")

        self.prehistory = QLineEdit()
        self.prehistory.setFixedWidth(100)
        self.prehistory.setPlaceholderText("Prehistory")

        self.loadAvatarButton = QPushButton("Load avatar")
        self.loadAvatarButton.clicked.connect(self.loadAvatarDialog)
        self.loadAvatarButton.setFixedWidth(100)

        self.grid.addWidget(self.name, 0, 0, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.lvl, 0, 1, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.avatar, 1, 0, 4, 1, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.loadAvatarButton, 5, 0, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.race, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.profession, 2, 1, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.prehistory, 3, 1, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.inspiration, 4, 1, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

    def loadAvatarDialog(self):
        file = QFileDialog.getOpenFileName(self, caption='Open file', filter="Image files (*.jpg *.png)")

        if len(file[0]) > 0:
            self.pixmap = SaveManager().loadPixmapFromFile(file[0])

            pixmap = QPixmap(100, 100)
            painter = QPainter(pixmap)

            painter.begin(pixmap)
            painter.drawPixmap(pixmap.rect(), self.pixmap)
            painter.end()

            self.pixmap = pixmap
            self.avatar.setPixmap(pixmap)
