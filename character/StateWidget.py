from PyQt6.QtCore import Qt, QSignalBlocker
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

        self.name = name

        layout.addWidget(QLabel(self.name), row, 0, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.value, row, 1, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.modifier, row, 2, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.saveThrow, row, 3, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.saveThrowModifier, row, 4, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)

    def getData(self):
        return {
            "value": self.value.text(),
            "modifier": self.modifier.text(),
            "saveThrow": self.saveThrow.text(),
            "saveThrowModifier": self.saveThrowModifier.isChecked(),
            "name": self.name
        }

    def setData(self, data: dict):
        self.value.setText(data["value"])
        self.modifier.setText(data["modifier"])
        self.saveThrow.setText(data["saveThrow"])
        with QSignalBlocker(self.saveThrowModifier) as blocker:
            self.saveThrowModifier.setChecked(data["saveThrowModifier"])
        self.name = data["name"]