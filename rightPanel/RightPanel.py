from PyQt6.QtCore import QSignalBlocker
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QHBoxLayout

from rightPanel.ChatWidget import ChatWidget
from rightPanel.DiceWidget import DiceWidget
from rightPanel.TimeWidget import TimeWidget


class RightPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.vertical_layout = QVBoxLayout()
        self.setFixedWidth(300)

        self.vertical_layout.addLayout(self.addCheckBoxes())
        self.vertical_layout.addLayout(self.addWeatherAndTime())
        self.diceWidget = DiceWidget(self)
        self.vertical_layout.addWidget(self.diceWidget)
        self.vertical_layout.addStretch(1)
        self.chatWidget = ChatWidget(self)
        self.vertical_layout.addWidget(self.chatWidget)
        self.vertical_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.vertical_layout)

    def addCheckBoxes(self):
        layout = QHBoxLayout()

        self.showGridCheckBox = QCheckBox("Grid")
        self.showGridCheckBox.setChecked(True)
        self.showGridCheckBox.stateChanged.connect(self.parent().canvas.setGridVisibility)
        layout.addWidget(self.showGridCheckBox)

        self.darknessCheckBox = QCheckBox("Darkness")
        self.darknessCheckBox.setChecked(True)
        self.darknessCheckBox.stateChanged.connect(self.parent().canvas.setDarknessVisibility)
        layout.addWidget(self.darknessCheckBox)

        self.caveCheckBox = QCheckBox("Cave")
        self.caveCheckBox.setChecked(False)
        self.caveCheckBox.stateChanged.connect(self.parent().canvas.networkProxy.caveSend)
        layout.addWidget(self.caveCheckBox)

        return layout

    def setCaveDarkness(self, value):
        with QSignalBlocker(self.caveCheckBox) as blocker:
            self.caveCheckBox.setChecked(value)
        self.parent().canvas.setCaveDarkness(value)

    def addWeatherAndTime(self):
        secondRow = QHBoxLayout()
        self.timeWidget = TimeWidget(self)
        secondRow.addWidget(self.timeWidget)

        return secondRow

    def setMaster(self):
        self.timeWidget.startTime()
