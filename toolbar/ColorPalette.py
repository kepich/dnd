from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QPushButton

COLORS = [
    '#000000', '#001eff', '#35e3e3', '#5ebb49', '#458352', '#dcd37b', '#ffd035',
    '#cc9245', '#a15c3e', '#a42f3b', '#ff0000', '#81588d', '#ffffff', "#5c5a5a"
]


class QPaletteButton(QPushButton):

    def __init__(self, color):
        super().__init__()
        self.setFixedSize(QSize(18, 18))
        self.color = color
        self.setStyleSheet("background-color: %s;" % color)
