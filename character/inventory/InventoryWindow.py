from PyQt6.QtWidgets import QMainWindow, QTabWidget

from character.inventory.ItemsBookWindow import ItemsBookWindow
from character.inventory.MyItemsWidget import MyItemsWidget


class InventoryWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Inventory")

        self.setMinimumWidth(1250)
        self.setMinimumHeight(700)

        self.myItems = MyItemsWidget(self)

        self.weaponBook = ItemsBookWindow(self)
        self.weaponBook.addRemoveSignal.connect(self.myItems.addSpellToMyBook)

        centralWidget = QTabWidget()

        centralWidget.addTab(self.myItems, "My items")
        centralWidget.addTab(self.weaponBook, "Weapons")

        self.setCentralWidget(centralWidget)

    def getData(self):
        return self.myItems.getData()

    def setData(self, data: dict):
        self.myItems.setData(data)
