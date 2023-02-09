from model.DrawableObject import DrawableObject
from model.Metadata import Metadata


class Message:
    def __init__(self, action=None, uuid=None, drawableObject: DrawableObject = None, dx=None, dy=None, meta: Metadata = None):
        self.action = action
        self.uuid = uuid
        self.drawableObject = None if drawableObject is None else drawableObject.serialize()
        self.dx = dx
        self.dy = dy
        self.meta = meta
