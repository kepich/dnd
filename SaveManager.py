import pickle
from os import listdir


class SaveManager:
    saves_path = "saves/"

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
