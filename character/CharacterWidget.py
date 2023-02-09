from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout

from character.BasicStatsWidget import BasicStatsWidget
from character.ButtonsWidget import ButtonsWidget
from character.InfoWidget import InfoWidget
from character.StablockWidget import StatBlockWidget
from dialog.LoadCharacterDialog import LoadCharacterDialog
from dialog.SaveDialog import SaveDialog
from utils.SaveManager import SaveManager


class CharacterWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.saveManager = SaveManager()

        self.hLayout = QHBoxLayout()
        self.hLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.hLayout)

        self.infoWidget = InfoWidget(self)
        self.infoWidget.lvl.textChanged.connect(self.lvlChangedAction)

        self.hLayout.addWidget(self.infoWidget, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.buttons = ButtonsWidget()
        self.bindButtons()

        self.basicStatsWidget = BasicStatsWidget(self.buttons)
        self.basicStatsWidget.hp.textChanged.connect(lambda _: self.infoWidget.updateCharacterSlot())
        self.hLayout.addWidget(self.basicStatsWidget, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.statblock = StatBlockWidget()

        self.statblock.strengthWidget.modifier.textChanged.connect(self.buttons.skills.updateStrengthValue)
        self.statblock.dexterityWidget.modifier.textChanged.connect(self.buttons.skills.updateDexterityValue)
        self.statblock.intelligenceWidget.modifier.textChanged.connect(self.buttons.skills.updateIntelligenceValue)
        self.statblock.wisdomWidget.modifier.textChanged.connect(self.buttons.skills.updateWisdomValue)
        self.statblock.charismaWidget.modifier.textChanged.connect(self.buttons.skills.updateCharismaValue)

        self.hLayout.addWidget(self.statblock, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

    def bindButtons(self):
        self.buttons.saveCharButton.clicked.connect(self.saveCharButtonSlot)
        self.buttons.loadCharButton.clicked.connect(self.loadCharButtonSlot)

    def loadCharButtonSlot(self):
        dlg = LoadCharacterDialog(self)
        if dlg.exec():
            loadedData = self.saveManager.loadCharacter(dlg.getChosenCharacter())
            self.setData(loadedData)

    def saveCharButtonSlot(self):
        dlg = SaveDialog(self)
        if dlg.exec():
            self.saveManager.saveCharacter(dlg.saveNameTextBox.text(), self.getData())

    def getData(self):
        return {
            "info": self.infoWidget.getData(),
            "inventory": self.buttons.getData(),
            "basicStats": self.basicStatsWidget.getData(),
            "statblock": self.statblock.getData()
        }

    def setData(self, data: dict):
        self.infoWidget.setData(data["info"])
        self.basicStatsWidget.setData(data["basicStats"])
        self.buttons.setData(data["inventory"])
        self.statblock.setData(data["statblock"])

    def lvlChangedAction(self, newLvl: str):
        if newLvl.isnumeric():
            profBonus = (int(newLvl) - 1) // 4 + 2
        else:
            profBonus = 0
        self.buttons.updateProficiencyBonus(profBonus)
        self.basicStatsWidget.updateProficiencyBonus(profBonus)
        self.statblock.updateProficiencyBonus(profBonus)
