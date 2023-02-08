import pickle
from os import listdir

from PyQt6.QtGui import QPixmap


class SaveManager:
    saves_path = "saves/"
    scenes_path = "scenes/"

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
