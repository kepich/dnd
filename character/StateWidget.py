from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QCheckBox


class StateWidget(QWidget):
    def __init__(self, name: str, layout: QGridLayout, row: int, parent=None):
        super().__init__(parent)

        self.value = QLineEdit("0")
        self.value.setFixedWidth(30)

        self.modifier = QLineEdit("0")
        self.modifier.setFixedWidth(30)

        self.saveThrow = QLineEdit("0")
        self.saveThrow.setFixedWidth(30)

        self.saveThrowModifier = QCheckBox()
        self.saveThrowModifier.setFixedWidth(30)

        layout.addWidget(QLabel(name), row, 0, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.value, row, 1, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.modifier, row, 2, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.saveThrow, row, 3, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.saveThrowModifier, row, 4, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
