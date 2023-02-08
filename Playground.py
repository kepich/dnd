from PyQt6.QtCore import Qt
from PyQt6.QtGui import QResizeEvent
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QGridLayout

from Canvas import Canvas
from character.CharacterWidget import CharacterWidget
from rightPanel.RightPanel import RightPanel
from toolbar.ColorPalette import *


class Playground(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.canvas = Canvas(self)
        self.rightPanel = RightPanel(self)

        self.gridLayout = QGridLayout()
        self.gridLayout.addWidget(self.canvas, 0, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.gridLayout.addWidget(self.rightPanel, 0, 1, Qt.AlignmentFlag.AlignRight)

        self.gridLayout.setRowStretch(1, 1)
        self.hLayout = QHBoxLayout()
        self.gridLayout.addLayout(self.hLayout, 2, 0, Qt.AlignmentFlag.AlignLeft)
        self.hLayout.addLayout(self.createPaletteWidget())
        self.charWidget = CharacterWidget(self)
        self.hLayout.addWidget(self.charWidget)

        self.gridLayout.setRowStretch(3, 1)

        self.setLayout(self.gridLayout)

    def createPaletteWidget(self):
        palette = QGridLayout()
        i = 0
        for c in COLORS:
            b = QPaletteButton(c)
            b.pressed.connect(lambda c=c: self.canvas.setPenColor(c))
            palette.addWidget(b, i % 8, i // 8)
            i += 1
        return palette

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.canvas.resizeEvent(a0)

    def storeGame(self) -> dict:
        return {
            "canvas": self.canvas.storeGame(),
            "weatherTime": self.rightPanel.timeWidget.getCurrentTimeData()
        }

    def storeScene(self) -> dict:
        return {"canvas": self.canvas.storeScene()}

    def restoreGame(self, data: dict):
        self.canvas.restoreGame(data["canvas"])

        if "weatherTime" in data.keys():
            self.rightPanel.timeWidget.setCurrentTimeData(data["weatherTime"])

        self.rightPanel.setCaveDarkness(data["canvas"]["isCave"])
