class Metadata:

    def __init__(self, isEntity: bool = False, hp: int = 0, name: str = None):
        self.isEntity = isEntity
        self.hp = hp
        self.name = name

    def serialize(self):
        res = {}
        if self.isEntity is not None:
            res["isEntity"] = self.isEntity
        if self.hp is not None:
            res["hp"] = self.hp
        if self.name is not None:
            res["name"] = self.name

        return res

    def deserialize(data: dict):
        res = Metadata()
        res.field = data.get("isEntity")
        res.hp = data.get("hp")
        res.name = data.get("name")

        return res

    def isEntityCheck(self):
        return self.isEntity
