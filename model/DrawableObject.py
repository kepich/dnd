import uuid

from PyQt6.QtCore import Qt, QRect

from model.Metadata import Metadata
from model.PixmapDto import PixmapDto


class DrawableObject:
    MIN_OBJECT_SIZE = 10

    def __init__(self, x_min, x_max, y_min, y_max, pixmap=None):
        self.q_rect = QRect(x_min, y_min, x_max - x_min, y_max - y_min)
        self.uuid = uuid.uuid1()
        self.pixmap = None
        if pixmap is not None:
            self.pixmap = pixmap
            self.pixmap.fill(Qt.GlobalColor.transparent)
        self.metadata = Metadata()

    def from_pixmap_and_offset(self, pixmap, x_offset, y_offset):
        self.q_rect = QRect(pixmap.rect())
        self.pixmap = pixmap
        self.move(x_offset, y_offset)

    def fit(self, x, y, line_width):
        self.q_rect.setX(min(self.q_rect.x(), x - line_width))
        self.q_rect.setWidth(max(self.q_rect.x() + self.q_rect.width(), x + line_width) - self.q_rect.x())

        self.q_rect.setY(min(self.q_rect.y(), y - line_width))
        self.q_rect.setHeight(max(self.q_rect.y() + self.q_rect.height(), y + line_width) - self.q_rect.y())

    def fit_pixmap(self):
        self.pixmap = self.pixmap.copy(self.q_rect)

    def move(self, x, y):
        self.q_rect.translate(x, y)

    def setPos(self, x, y):
        self.q_rect.moveTo(x, y)

    def setSize(self, width, height):
        self.q_rect.setWidth(width)
        self.q_rect.setHeight(height)

    def resize(self, x, y):
        new_w = max(self.MIN_OBJECT_SIZE, self.q_rect.width() + x)
        new_h = max(self.MIN_OBJECT_SIZE, self.q_rect.height() + y)

        self.q_rect.setWidth(new_w)
        self.q_rect.setHeight(new_h)

    def isContains(self, x, y):
        return self.q_rect.contains(x, y)

    def serialize(self):
        res = {
            "q_rect": self.q_rect,
            "uuid": self.uuid,
            "pixmapDto": PixmapDto(self.pixmap)
        }

        if self.metadata is not None:
            res["meta"] = self.metadata.serialize()

        return res

    def deserialize(dictionary: dict):
        res = DrawableObject(0, 0, 0, 0)
        res.q_rect = dictionary["q_rect"]
        res.pixmap = dictionary["pixmapDto"].pixmap
        res.uuid = dictionary["uuid"]
        if "meta" in dictionary.keys():
            res.metadata = Metadata.deserialize(dictionary["meta"])
        return res

    def isEntity(self):
        return self.metadata.isEntityCheck()

    def getEntityHeader(self):
        if self.metadata.isEntityCheck():
            return f"{self.metadata.name} {self.metadata.hp} HP"
        else:
            return ""

    def stickToGrid(self, gridStep):
        if self.isEntity():
            self.q_rect.moveTo(round(self.q_rect.x() / gridStep) * gridStep,
                               round(self.q_rect.y() / gridStep) * gridStep)
