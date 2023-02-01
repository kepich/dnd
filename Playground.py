from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from Canvas import Canvas
from ColorPalette import *


class Playground(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedSize(QSize(1000, 800))
        self.setStyleSheet("border: 1px solid black;")

        self.canvas = Canvas(self)

        self.createPaletteWidget()

    def createPaletteWidget(self):
        vertical_layout = QVBoxLayout()
        self.setLayout(vertical_layout)
        vertical_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        vertical_layout.addWidget(self.canvas)
        palette = QHBoxLayout()
        self.addPaletteButtons(palette)
        vertical_layout.addLayout(palette)

    def addPaletteButtons(self, layout):
        for c in COLORS:
            b = QPaletteButton(c)
            b.pressed.connect(lambda c=c: self.canvas.setPenColor(c))
            layout.addWidget(b)
