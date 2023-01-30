from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt

from Canvas import Canvas
from ColorPalette import *


class Playground(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("DnD")
        self.setGeometry(100, 100, 600, 400)

        self.canvas = Canvas()

        self.createPaletteWidget()

    def createPaletteWidget(self):
        vertical_layout = QVBoxLayout()
        self.setLayout(vertical_layout)
        vertical_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        vertical_layout.addWidget(self.canvas)
        palette = QHBoxLayout()
        self.add_palette_buttons(palette)
        vertical_layout.addStretch()
        vertical_layout.addLayout(palette)

    def add_palette_buttons(self, layout):
        for c in COLORS:
            b = QPaletteButton(c)
            b.pressed.connect(lambda c=c: self.canvas.set_pen_color(c))
            layout.addWidget(b)
