from PyQt6.QtCore import Qt, QSignalBlocker, pyqtSignal
from PyQt6.QtGui import QPainter, QPixmap, QIntValidator
from PyQt6.QtWidgets import QWidget, QLineEdit, QCheckBox, QGridLayout, QPushButton, QFileDialog

from model.Metadata import Metadata
from model.PixmapDto import PixmapDto
from utils.QClickableLabel import QClickableLabel
from utils.SaveManager import SaveManager


class InfoWidget(QWidget):
    pasteCharacter = pyqtSignal(QPixmap, Metadata)
    updateCharacter = pyqtSignal(Metadata)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid = QGridLayout()
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setVerticalSpacing(0)

        self.setLayout(self.grid)

        self.pixmap = None
        self.avatar = QClickableLabel("Avatar")
        self.avatar.setFixedHeight(100)
        self.avatar.setFixedWidth(100)
        self.avatar.click.connect(self.copyAvatar)

        self.name = QLineEdit()
        self.name.setFixedWidth(100)
        self.name.setPlaceholderText("Nickname")

        self.lvl = QLineEdit()
        self.lvl.setFixedWidth(45)
        self.lvl.setValidator(QIntValidator(0, 90, self))
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
        self.grid.addWidget(self.loadAvatarButton, 5, 0,
                            alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.race, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.profession, 2, 1, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.prehistory, 3, 1, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.inspiration, 4, 1, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

    def loadAvatarDialog(self):
        file = QFileDialog.getOpenFileName(self, caption='Open file', filter="Image files (*.jpg *.png)")

        if len(file[0]) > 0:
            self.pixmap = SaveManager().loadPixmapFromFile(file[0])

            pixmap = QPixmap(100, 100)
            pixmap.fill(Qt.GlobalColor.transparent)
            painter = QPainter(pixmap)

            painter.begin(pixmap)
            painter.drawPixmap(pixmap.rect(), self.pixmap)
            painter.end()

            self.pixmap = pixmap
            self.avatar.setPixmap(pixmap)

    def copyAvatar(self):
        meta = self.getMetadata()
        if meta is not None:
            self.pasteCharacter.emit(self.pixmap, meta)

    def updateCharacterSlot(self):
        meta = self.getMetadata()
        if meta is not None:
            self.updateCharacter.emit(meta)

    def getMetadata(self):
        if self.pixmap is not None and self.parent().basicStatsWidget.hp.text().isnumeric() and self.name.text() != "":
            return Metadata(True, int(self.parent().basicStatsWidget.hp.text()), self.name.text())
        return None

    def getData(self):
        return {
            "pixmap": PixmapDto(self.pixmap),
            "name": self.name.text(),
            "lvl": self.lvl.text(),
            "race": self.race.text(),
            "profession": self.profession.text(),
            "armorClass": self.armorClass.text(),
            "inspiration": self.inspiration.isChecked(),
            "prehistory": self.prehistory.text()
        }

    def setData(self, data: dict):
        self.pixmap = data["pixmap"].pixmap
        self.avatar.setPixmap(self.pixmap)
        self.name.setText(data["name"])
        self.lvl.setText(data["lvl"])
        self.race.setText(data["race"])
        self.profession.setText(data["profession"])
        self.armorClass.setText(data["armorClass"])
        with QSignalBlocker(self.inspiration) as blocker:
            self.inspiration.setChecked(data["inspiration"])
        self.prehistory.setText(data["prehistory"])
