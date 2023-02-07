import random
import time

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel, QVBoxLayout, QListWidget


class DiceWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)

        self.diceListLabel = QLabel("")
        self.diceListLabel.setWordWrap(True)
        self.diceListLabel.setFixedHeight(15)
        self.diceListLabel.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.verticalLayout.addWidget(self.diceListLabel)

        self.numerOfDiceList = self.createNumberOfDiceList()
        self.verticalLayout.addWidget(self.numerOfDiceList)
        self.verticalLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout = QGridLayout()
        self.verticalLayout.addLayout(self.gridLayout)
        self.gridLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.d20 = QPushButton("20")
        self.d20.pressed.connect(lambda: self.throwDice(20))
        self.d4 = QPushButton("4")
        self.d4.pressed.connect(lambda: self.throwDice(4))
        self.d6 = QPushButton("6")
        self.d6.pressed.connect(lambda: self.throwDice(6))
        self.d8 = QPushButton("8")
        self.d8.pressed.connect(lambda: self.throwDice(8))
        self.d10 = QPushButton("10")
        self.d10.pressed.connect(lambda: self.throwDice(10))
        self.d12 = QPushButton("12")
        self.d12.pressed.connect(lambda: self.throwDice(12))
        self.diceResultLabel = QLabel("0")
        self.diceResultLabel.setFixedWidth(30)

        self.gridLayout.addWidget(self.d20, 0, 0)
        self.gridLayout.addWidget(self.d12, 0, 1)
        self.gridLayout.addWidget(self.d10, 0, 2)
        self.gridLayout.addWidget(self.d8, 1, 0)
        self.gridLayout.addWidget(self.d4, 1, 1)
        self.gridLayout.addWidget(self.d6, 1, 2)
        self.gridLayout.addWidget(self.diceResultLabel, 0, 3, 2, 1, alignment=Qt.AlignmentFlag.AlignCenter)

    def createNumberOfDiceList(self):
        res = QListWidget(self)
        res.setFlow(QListWidget.Flow.LeftToRight)
        res.addItems([f"{i + 1}" for i in range(10)])
        res.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        res.setCurrentRow(0)
        res.setMaximumHeight(30)
        res.setStyleSheet("QScrollBar {width:0px;}")

        for i in range(res.count()):
            item = res.item(i)
            item.setSizeHint(QSize(27, 20))

        return res

    def throwDice(self, maxValue):
        random.seed(time.time())

        selected = int(self.numerOfDiceList.selectedItems()[0].text())
        values = []
        for i in range(selected):
            values.append(random.randint(1, maxValue))

        summa = str(sum(values))

        if selected > 1:
            res = f"{values[0]}" + ''.join([f", {i}" for i in values[1:]])
            self.diceListLabel.setText(res)
            self.parent().parent().canvas.networkProxy.sendMessageToChat(res + f" = {summa}")
        else:
            self.diceListLabel.setText("")
            self.parent().parent().canvas.networkProxy.sendMessageToChat(summa)

        self.diceResultLabel.setText(summa)
