from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton

from character.NotebookWidget import NotebookWidget


class ButtonsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.grid = QGridLayout()
        # self.grid.setVerticalSpacing(0)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.grid)

        self.inventoryButton = QPushButton("Inventory")
        self.inventory = NotebookWidget(name="Inventory")
        self.inventoryButton.clicked.connect(self.inventory.show)

        self.magicButton = QPushButton("Magic")
        self.magic = NotebookWidget(name="Magic")
        self.magicButton.clicked.connect(self.magic.show)

        self.skillsButton = QPushButton("Skills")
        self.skills = NotebookWidget(name="Skills")
        self.skillsButton.clicked.connect(self.skills.show)

        self.notebookButton = QPushButton("Notebook")
        self.notebook = NotebookWidget(name="Notebook")
        self.notebookButton.clicked.connect(self.notebook.show)

        self.saveCharButton = QPushButton("Save char")
        self.saveCharButton.clicked.connect(self.notebook.show)

        self.loadCharButton = QPushButton("Load char")
        self.loadCharButton.clicked.connect(self.notebook.show)

        self.grid.addWidget(self.inventoryButton, 0, 0)
        self.grid.addWidget(self.magicButton, 0, 1)
        self.grid.addWidget(self.skillsButton, 1, 0)
        self.grid.addWidget(self.notebookButton, 1, 1)
        self.grid.addWidget(self.saveCharButton, 2, 0)
        self.grid.addWidget(self.loadCharButton, 2, 1)
