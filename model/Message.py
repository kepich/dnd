from model.DrawableObject import DrawableObject


class Message:
    def __init__(self, action=None, uuid=None, drawableObject: DrawableObject = None, dx=None, dy=None):
        self.action = action
        self.uuid = uuid
        self.drawableObject = None if drawableObject is None else drawableObject.serialize()
        self.dx = dx
        self.dy = dy

    def __str__(self):
        return "{" + f"action={self.action}, " \
                     f"uuid={self.uuid}, " \
                     f"drawableObject={self.drawableObject}, " \
                     f"dx={self.dx}, " \
                     f"dy={self.dx}" + "}"
