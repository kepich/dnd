from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QGridLayout, QLineEdit, QCheckBox, QPushButton

from character.NotebookWidget import NotebookWidget


class StatblockWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.grid = QGridLayout()
        self.grid.setVerticalSpacing(0)
        self.grid.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.grid)

        self.strengthLabel = QLabel("STR")
        self.dexterityLabel = QLabel("DEX")
        self.constitutionLabel = QLabel("CONST")
        self.intelligenceLabel = QLabel("INT")
        self.wisdomLabel = QLabel("WSD")
        self.charismaLabel = QLabel("CHR")

        self.grid.addWidget(self.strengthLabel, 0, 1, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        self.grid.addWidget(self.dexterityLabel, 0, 3, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        self.grid.addWidget(self.constitutionLabel, 0, 5, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        self.grid.addWidget(self.intelligenceLabel, 0, 7, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        self.grid.addWidget(self.wisdomLabel, 0, 9, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        self.grid.addWidget(self.charismaLabel, 0, 11, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)

        self.grid.addWidget(QLabel("Val/Mod"), 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        self.grid.addWidget(QLabel("Save Throw"), 2, 0, alignment=Qt.AlignmentFlag.AlignCenter)

        self.strengthEdit = QLineEdit("0")
        self.strengthEdit.setFixedWidth(30)
        self.strengthModifierEdit = QLineEdit("0")
        self.strengthModifierEdit.setFixedWidth(30)

        self.dexterityEdit = QLineEdit("0")
        self.dexterityEdit.setFixedWidth(30)
        self.dexterityModifierEdit = QLineEdit("0")
        self.dexterityModifierEdit.setFixedWidth(30)

        self.constitutionEdit = QLineEdit("0")
        self.constitutionEdit.setFixedWidth(30)
        self.constitutionModifierEdit = QLineEdit("0")
        self.constitutionModifierEdit.setFixedWidth(30)

        self.intelligenceEdit = QLineEdit("0")
        self.intelligenceEdit.setFixedWidth(30)
        self.intelligenceModifierEdit = QLineEdit("0")
        self.intelligenceModifierEdit.setFixedWidth(30)

        self.wisdomEdit = QLineEdit("0")
        self.wisdomEdit.setFixedWidth(30)
        self.wisdomModifierEdit = QLineEdit("0")
        self.wisdomModifierEdit.setFixedWidth(30)

        self.charismaEdit = QLineEdit("0")
        self.charismaEdit.setFixedWidth(30)
        self.charismaModifierEdit = QLineEdit("0")
        self.charismaModifierEdit.setFixedWidth(30)

        self.grid.addWidget(self.strengthEdit, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.strengthModifierEdit, 1, 2, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.grid.addWidget(self.dexterityEdit, 1, 3, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.dexterityModifierEdit, 1, 4, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.grid.addWidget(self.constitutionEdit, 1, 5, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.constitutionModifierEdit, 1, 6, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.grid.addWidget(self.intelligenceEdit, 1, 7, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.intelligenceModifierEdit, 1, 8, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.grid.addWidget(self.wisdomEdit, 1, 9, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.wisdomModifierEdit, 1, 10, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.grid.addWidget(self.charismaEdit, 1, 11, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.charismaModifierEdit, 1, 12, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        
        self.strengthSaveThrowEdit = QLineEdit("0")
        self.strengthSaveThrowEdit.setFixedWidth(30)
        self.strengthSaveThrowModifier = QCheckBox()
        self.strengthSaveThrowModifier.setFixedWidth(30)

        self.dexteritySaveThrowEdit = QLineEdit("0")
        self.dexteritySaveThrowEdit.setFixedWidth(30)
        self.dexteritySaveThrowModifier = QCheckBox()
        self.dexteritySaveThrowModifier.setFixedWidth(30)

        self.constitutionSaveThrowEdit = QLineEdit("0")
        self.constitutionSaveThrowEdit.setFixedWidth(30)
        self.constitutionSaveThrowModifier = QCheckBox()
        self.constitutionSaveThrowModifier.setFixedWidth(30)

        self.intelligenceSaveThrowEdit = QLineEdit("0")
        self.intelligenceSaveThrowEdit.setFixedWidth(30)
        self.intelligenceSaveThrowModifier = QCheckBox()
        self.intelligenceSaveThrowModifier.setFixedWidth(30)

        self.wisdomSaveThrowEdit = QLineEdit("0")
        self.wisdomSaveThrowEdit.setFixedWidth(30)
        self.wisdomSaveThrowModifier = QCheckBox()
        self.wisdomSaveThrowModifier.setFixedWidth(30)

        self.charismaSaveThrowEdit = QLineEdit("0")
        self.charismaSaveThrowEdit.setFixedWidth(30)
        self.charismaSaveThrowModifier = QCheckBox()
        self.charismaSaveThrowModifier.setFixedWidth(30)
        
        self.grid.addWidget(self.strengthSaveThrowEdit, 2, 1, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.strengthSaveThrowModifier, 2, 2, alignment=Qt.AlignmentFlag.AlignCenter)

        self.grid.addWidget(self.dexteritySaveThrowEdit, 2, 3, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.dexteritySaveThrowModifier, 2, 4, alignment=Qt.AlignmentFlag.AlignCenter)

        self.grid.addWidget(self.constitutionSaveThrowEdit, 2, 5, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.constitutionSaveThrowModifier, 2, 6, alignment=Qt.AlignmentFlag.AlignCenter)

        self.grid.addWidget(self.intelligenceSaveThrowEdit, 2, 7, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.intelligenceSaveThrowModifier, 2, 8, alignment=Qt.AlignmentFlag.AlignCenter)

        self.grid.addWidget(self.wisdomSaveThrowEdit, 2, 9, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.wisdomSaveThrowModifier, 2, 10, alignment=Qt.AlignmentFlag.AlignCenter)

        self.grid.addWidget(self.charismaSaveThrowEdit, 2, 11, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.charismaSaveThrowModifier, 2, 12, alignment=Qt.AlignmentFlag.AlignCenter)

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

        self.grid.addWidget(self.inventoryButton, 3, 3, 1, 2)
        self.grid.addWidget(self.magicButton, 3, 5, 1, 2)
        self.grid.addWidget(self.skillsButton, 3, 7, 1, 2)
        self.grid.addWidget(self.notebookButton, 3, 9, 1, 2)