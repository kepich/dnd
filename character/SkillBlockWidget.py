from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel

from character.Skill import Skill


class SkillBlockWidget(QWidget):
    def __init__(self, gridLayout: QGridLayout, starRow: int, skills: list, name: str, parent=None):
        super().__init__(parent)

        gridLayout.addWidget(QLabel(name), starRow, 0, 1, 3,
                             alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.skills = []
        self.name = name

        for i in range(len(skills)):
            self.skills.append(Skill(gridLayout, starRow + i + 1, skills[i]))

    def getData(self):
        return {skill.name.text(): skill.getData() for skill in self.skills}

    def setData(self, data: dict):
        for key, value in data.items():
            next(filter(lambda sk: sk.name.text() == key, self.skills)).setData(value)

    def updateProficiencyBonus(self, newBonus):
        for skill in self.skills:
            skill.updateProficiencyBonus(newBonus)

    def updateValue(self, param):
        for skill in self.skills:
            skill.updateStatValue(param)
