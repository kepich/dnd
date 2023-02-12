from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGridLayout, QLabel, QCheckBox


class Skill:
    def __init__(self, gridLayout: QGridLayout, row: int, name: str):
        self.name = QLabel(name)
        self.value = QLabel("0")
        self.modifier = QCheckBox()
        self.modifier.stateChanged.connect(lambda _: self.recalculateValue())
        self.profBonus = 0
        self.statValue = 0

        gridLayout.addWidget(self.name, row, 0, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        gridLayout.addWidget(self.value, row, 1, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        gridLayout.addWidget(self.modifier, row, 2, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

    def getData(self):
        return {
            "name": self.name.text(),
            "value": self.value.text(),
            "modifier": self.modifier.isChecked(),
            "profBonus": self.profBonus
        }

    def setData(self, data: dict):
        self.statValue = int(data["value"])
        self.profBonus = data["profBonus"]
        self.modifier.setChecked(data["modifier"])

    def updateProficiencyBonus(self, newBonus):
        self.profBonus = newBonus
        self.recalculateValue()

    def updateStatValue(self, newValue):
        self.statValue = newValue
        self.recalculateValue()

    def recalculateValue(self):
        value = self.statValue
        if self.modifier.isChecked():
            value += self.profBonus

        self.value.setText(str(value))
