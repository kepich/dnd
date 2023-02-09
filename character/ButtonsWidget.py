from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton

from character.NotebookWidget import NotebookWidget
from character.SkillsWidget import SkillsWidget


class ButtonsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.grid = QGridLayout()
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.grid)

        self.inventoryButton = QPushButton("Inventory")
        self.inventory = NotebookWidget(name="Inventory")
        self.inventoryButton.clicked.connect(self.inventory.show)

        self.magicButton = QPushButton("Magic")
        self.magic = NotebookWidget(name="Magic")
        self.magicButton.clicked.connect(self.magic.show)

        self.skillsButton = QPushButton("Skills")
        self.skills = SkillsWidget(name="Skills")
        self.skillsButton.clicked.connect(self.skills.show)

        self.notebookButton = QPushButton("Notebook")
        self.notebook = NotebookWidget(name="Notebook")
        self.notebookButton.clicked.connect(self.notebook.show)

        self.saveCharButton = QPushButton("Save char")
        self.loadCharButton = QPushButton("Load char")

        self.grid.addWidget(self.inventoryButton, 0, 0)
        self.grid.addWidget(self.magicButton, 0, 1)
        self.grid.addWidget(self.skillsButton, 1, 0)
        self.grid.addWidget(self.notebookButton, 1, 1)
        self.grid.addWidget(self.saveCharButton, 2, 0)
        self.grid.addWidget(self.loadCharButton, 2, 1)

    def updateProficiencyBonus(self, newBonus: int):
        self.skills.updateProficiencyBonus(newBonus)
        pass

    def getData(self):
        return {
            "inventory": self.inventory.getData(),
            "magic": self.magic.getData(),
            "skills": self.skills.getData(),
            "notebook": self.notebook.getData()
        }

    def setData(self, data: dict):
        self.inventory.setData(data["inventory"])
        self.magic.setData(data["magic"])
        self.skills.setData(data["skills"])
        self.notebook.setData(data["notebook"])
