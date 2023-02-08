import pickle
from os import listdir

from PyQt6.QtGui import QPixmap


class SaveManager:
    saves_path = "data/saves/"
    scenes_path = "data/scenes/"
    characters_path = "data/characters/"

    def save(self, saveName: str, data: dict):
        file_name = f'{self.saves_path}{saveName}.save'
        f = open(file_name, 'wb')
        f.write(pickle.dumps(data))
        f.close()

    def load(self, saveName: str) -> dict:
        file_name = f'{self.saves_path}{saveName}'
        f = open(file_name, 'rb')
        return pickle.loads(f.read())

    def getSaves(self):
        return [f for f in listdir(self.saves_path)]

    def saveScene(self, sceneName: str, data: dict):
        file_name = f'{self.scenes_path}{sceneName}.scene'
        f = open(file_name, 'wb')
        f.write(pickle.dumps(data))
        f.close()

    def loadScene(self, sceneName: str) -> dict:
        file_name = f'{self.scenes_path}{sceneName}'
        f = open(file_name, 'rb')
        return pickle.loads(f.read())

    def getScenes(self):
        return [f for f in listdir(self.scenes_path)]

    def loadPixmapFromFile(self, filename: str) -> QPixmap:
        return QPixmap(filename)

    def saveCharacter(self, characterName: str, data: dict):
        file_name = f'{self.characters_path}{characterName}.char'
        f = open(file_name, 'wb')
        f.write(pickle.dumps(data))
        f.close()

    def loadCharacter(self, characterName: str) -> dict:
        file_name = f'{self.characters_path}{characterName}'
        f = open(file_name, 'rb')
        return pickle.loads(f.read())

    def getCharacters(self):
        return [f for f in listdir(self.characters_path)]
