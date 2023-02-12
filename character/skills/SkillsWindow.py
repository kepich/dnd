from PyQt6 import QtGui
from PyQt6.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QLabel, QHBoxLayout, QGridLayout, QMainWindow

from character.skills.SkillBlockWidget import SkillBlockWidget


class SkillsWindow(QMainWindow):
    def __init__(self, parent=None, name: str = ""):
        super().__init__(parent)

        self.data = ""
        self.skills = {
            "STR": ["Атлетика"],
            "DEX": ["Акробатика", "Ловкость рук", "Скрытность"],
            "INT": ["Анализ", "История", "Магия", "Природа", "Религия"],
            "WSD": ["Внимательность", "Выживание", "Медицина", "Проницательность", "Уход за животными"],
            "CHR": ["Выступление", "Запугивание", "Обман", "Убеждение"]
        }

        layout = QVBoxLayout()
        layout.addWidget(QLabel(name))

        hLayout = QHBoxLayout()

        gridLayout = QGridLayout()
        self.skillBlock = []

        row = 0
        for key, value in self.skills.items():
            self.skillBlock.append(SkillBlockWidget(gridLayout, row, value, key))
            row += len(value) + 1

        hLayout.addLayout(gridLayout)

        self.textEdit = QTextEdit()
        self.textEdit.setFixedWidth(600)
        hLayout.addWidget(self.textEdit)

        layout.addLayout(hLayout)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.data = self.textEdit.toPlainText()
        a0.accept()

    def getData(self):
        return {
            "data": self.data,
            "skills": {skill.name: skill.getData() for skill in self.skillBlock}
        }

    def setData(self, data: dict):
        self.data = data["data"]
        self.textEdit.setText(data["data"])

        for key, value in data["skills"].items():
            next(filter(lambda sk: sk.name == key, self.skillBlock)).setData(value)

    def updateProficiencyBonus(self, newBonus):
        for sb in self.skillBlock:
            sb.updateProficiencyBonus(newBonus)

    def updateStrengthValue(self, newValue: str):
        next(filter(lambda sb: sb.name == "STR", self.skillBlock)).updateValue(int(newValue))

    def updateDexterityValue(self, newValue: str):
        next(filter(lambda sb: sb.name == "DEX", self.skillBlock)).updateValue(int(newValue))

    def updateIntelligenceValue(self, newValue: str):
        next(filter(lambda sb: sb.name == "INT", self.skillBlock)).updateValue(int(newValue))

    def updateWisdomValue(self, newValue: str):
        next(filter(lambda sb: sb.name == "WSD", self.skillBlock)).updateValue(int(newValue))

    def updateCharismaValue(self, newValue: str):
        next(filter(lambda sb: sb.name == "CHR", self.skillBlock)).updateValue(int(newValue))
