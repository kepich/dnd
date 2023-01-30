from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollArea

from Canvas import Canvas
from ColorPalette import *


class Playground(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("DnD")
        self.setGeometry(parent.geometry())

        self.canvas = Canvas()

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(self.canvas)

        self.create_palette_widget()

    def create_palette_widget(self):
        vertical_layout = QVBoxLayout()
        self.setLayout(vertical_layout)
        vertical_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        vertical_layout.addWidget(self.scrollArea)
        palette = QHBoxLayout()
        self.add_palette_buttons(palette)
        vertical_layout.addLayout(palette)

    def add_palette_buttons(self, layout):
        for c in COLORS:
            b = QPaletteButton(c)
            b.pressed.connect(lambda c=c: self.canvas.set_pen_color(c))
            layout.addWidget(b)
