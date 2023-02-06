from PyQt6.QtCore import Qt
from PyQt6.QtGui import QResizeEvent
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QGridLayout

from Canvas import Canvas
from ColorPalette import *
from RightPanel import RightPanel


class Playground(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.canvas = Canvas(self)
        self.createPaletteWidget()
        self.rightPanel = RightPanel(self)

        self.gridLayout = QGridLayout()
        self.gridLayout.addWidget(self.canvas, 0, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.gridLayout.addWidget(self.rightPanel, 0, 1, Qt.AlignmentFlag.AlignRight)

        self.gridLayout.setRowStretch(1, 1)
        self.gridLayout.addLayout(self.palette, 2, 0)

        self.gridLayout.setRowStretch(3, 1)

        self.setLayout(self.gridLayout)

    def createPaletteWidget(self):
        self.palette = QHBoxLayout()
        self.addPaletteButtons(self.palette)

    def addPaletteButtons(self, layout):
        for c in COLORS:
            b = QPaletteButton(c)
            b.pressed.connect(lambda c=c: self.canvas.setPenColor(c))
            layout.addWidget(b)

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.canvas.resizeEvent(a0)

    def storeGame(self) -> dict:
        return {
            "canvas": self.canvas.storeGame(),
            "weatherTime": self.rightPanel.timeWidget.getCurrentTimeData()
        }

    def restoreGame(self, data: dict):
        self.canvas.restoreGame(data["canvas"])
        self.rightPanel.timeWidget.setCurrentTimeData(data["weatherTime"])
