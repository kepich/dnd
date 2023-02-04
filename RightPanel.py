from PyQt6.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QHBoxLayout, QListWidget

from ChatWidget import ChatWidget
from DiceWidget import DiceWidget
from TimeWidget import TimeWidget


class RightPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.vertical_layout = QVBoxLayout()
        self.setFixedWidth(300)

        self.addElements()
        self.vertical_layout.addLayout(self.addWeatherAndTime())
        self.vertical_layout.addStretch(1)
        self.diceWidget = DiceWidget(self)
        self.vertical_layout.addWidget(self.diceWidget)
        self.vertical_layout.addStretch(1)
        self.chatWidget = ChatWidget()
        self.vertical_layout.addWidget(self.chatWidget)
        self.vertical_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.vertical_layout)

    def addElements(self):
        firstRow = QHBoxLayout()
        self.addCheckBoxes(firstRow)
        self.vertical_layout.addLayout(firstRow)

    def addCheckBoxes(self, layout):
        self.showGridCheckBox = QCheckBox("Grid")
        self.showGridCheckBox.setChecked(True)
        self.showGridCheckBox.stateChanged.connect(self.parent().canvas.setGridVisibility)
        layout.addWidget(self.showGridCheckBox)

        self.darknessCheckBox = QCheckBox("Darkness")
        layout.addWidget(self.darknessCheckBox)

    def addWeatherAndTime(self):
        secondRow = QHBoxLayout()
        self.timeWidget = TimeWidget()
        self.timeWidget.startTime()
        secondRow.addWidget(self.timeWidget)
        # secondRow.addWidget(secondRow)

        return secondRow
