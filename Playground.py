from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from Canvas import Canvas
from ColorPalette import *
from RightPanel import RightPanel


class Playground(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.canvas = Canvas(self)
        self.rightPanel = RightPanel(self)

        self.createPaletteWidget()

    def createPaletteWidget(self):
        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.addWidget(self.canvas)
        self.palette = QHBoxLayout()
        self.addPaletteButtons(self.palette)
        self.vertical_layout.addStretch(1)
        self.vertical_layout.addLayout(self.palette)

        self.horizontal_layout = QHBoxLayout()
        self.setLayout(self.horizontal_layout)
        self.horizontal_layout.addLayout(self.vertical_layout)
        self.horizontal_layout.addStretch(1)
        self.horizontal_layout.addWidget(self.rightPanel)

    def addPaletteButtons(self, layout):
        for c in COLORS:
            b = QPaletteButton(c)
            b.pressed.connect(lambda c=c: self.canvas.setPenColor(c))
            layout.addWidget(b)
