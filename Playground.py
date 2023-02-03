from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QGridLayout

from Canvas import Canvas
from ColorPalette import *
from RightPanel import RightPanel


class Playground(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        print(f"{self.width()}, {self.height()}")

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
