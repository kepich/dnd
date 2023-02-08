from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout

from character.BasicStatsWidget import BasicStatsWidget
from character.ButtonsWidget import ButtonsWidget
from character.InfoWidget import InfoWidget
from character.StablockWidget import StatblockWidget



class CharacterWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.hLayout = QHBoxLayout()
        self.hLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.hLayout)

        self.infoWidget = InfoWidget()
        self.hLayout.addWidget(self.infoWidget, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.buttons = ButtonsWidget()

        self.basicStatsWidget = BasicStatsWidget(self.buttons)
        self.hLayout.addWidget(self.basicStatsWidget, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.statblock = StatblockWidget()
        self.hLayout.addWidget(self.statblock, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

