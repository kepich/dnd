import pickle

from DrawableObject import DrawableObject


class FirstLoadDto:
    def __init__(self, objects: list[DrawableObject]):
        if objects is None:
            self.objects = None
        else:
            self.objects = [obj.serialize() for obj in objects]

    def fromBytes(bytes):
        dto = pickle.loads(bytes)
        dto.objects = [DrawableObject.deserialize(i) for i in dto.objects]
        return dto
