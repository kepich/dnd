from PyQt6 import QtGui
from PyQt6.QtWidgets import QWidget, QScrollArea, QHBoxLayout, QVBoxLayout, QTextEdit

from character.inventory.ItemWidget import ItemWidget


class MyItemsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = ""

        hLayout = QHBoxLayout()
        self.myItems = []

        self.scrollAreaLeft = QScrollArea()
        self.scrollAreaWidget = QWidget()
        self.scrollAreaLeft.setWidget(self.scrollAreaWidget)
        hLayout.addWidget(self.scrollAreaLeft)

        self.scrollAreaRight = QScrollArea()

        self.otherItems = QTextEdit()
        vLayoutR = QVBoxLayout()
        vLayoutR.addWidget(self.otherItems)
        self.scrollAreaRight.setLayout(vLayoutR)
        hLayout.addWidget(self.scrollAreaRight)

        layout = QVBoxLayout()

        layout.addLayout(hLayout)

        self.setLayout(layout)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.data = self.otherItems.toPlainText()
        a0.accept()

    def getData(self):
        return {
            "data": self.data,
            "items": self.myItems
        }

    def setData(self, data: dict):
        self.data = data["data"]
        if "items" in data.keys():
            self.myItems = data["items"]
        self.otherItems.setText(data["data"])
        self.redrawSpells()

    def addSpellToMyBook(self, cast):
        self.myItems.append(cast)
        self.redrawSpells()

    def redrawSpells(self):
        vLayout = QVBoxLayout()
        for item in self.myItems:
            itemWidget = ItemWidget(item, isAdded=True)
            itemWidget.removeSignal.connect(self.removeItem)
            vLayout.addWidget(itemWidget)
        self.scrollAreaWidget = QWidget()
        self.scrollAreaWidget.setLayout(vLayout)
        self.scrollAreaLeft.setWidget(self.scrollAreaWidget)

    def removeItem(self, cast):
        self.myItems.remove(cast)
        self.redrawSpells()
