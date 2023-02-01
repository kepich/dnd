from enum import Enum


class Action(Enum):
    MOVE = 1
    RESIZE = 2
    CREATE = 3
    REMOVE = 4
    CLEAR = 5


class Message:
    def __init__(self, action, uuid=None, drawableObject=None, dx=None, dy=None):
        self.action = action
        self.uuid = uuid
        self.drawableObject = drawableObject
        self.dx = dx
        self.dy = dy

    def __str__(self):
        return "{" + f"action={self.action}, " \
                     f"uuid={self.uuid}, " \
                     f"drawableObject={self.drawableObject}, " \
                     f"dx={self.dx}, " \
                     f"dy={self.dx}" + "}"