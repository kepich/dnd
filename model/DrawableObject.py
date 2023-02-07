import uuid

from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QPixmap


class DrawableObject:
    MIN_OBJECT_SIZE = 10

    def __init__(self, x_min, x_max, y_min, y_max, pixmap):
        self.q_rect = QRect(x_min, y_min, x_max - x_min, y_max - y_min)
        self.uuid = uuid.uuid1()
        self.pixmap = pixmap
        self.pixmap.fill(Qt.GlobalColor.transparent)

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
        self.q_rect.setX(self.q_rect.x() + x)
        self.q_rect.setRight(self.q_rect.right() + x)
        self.q_rect.setY(self.q_rect.y() + y)
        self.q_rect.setBottom(self.q_rect.bottom() + y)

    def resize(self, x, y):
        new_w = max(self.MIN_OBJECT_SIZE, self.q_rect.width() + x)
        new_h = max(self.MIN_OBJECT_SIZE, self.q_rect.height() + y)

        self.q_rect.setWidth(new_w)
        self.q_rect.setHeight(new_h)

    def is_collide(self, x, y):
        return self.q_rect.x() < x < self.q_rect.x() + self.q_rect.width() and \
               self.q_rect.y() < y < self.q_rect.y() + self.q_rect.height()

    def serialize(self):
        return {
            "q_rect": self.q_rect,
            "uuid": self.uuid,
            "pixmapDto": PixmapDto(self.pixmap)
        }

    def deserialize(dictionary: dict):
        res = DrawableObject(0, 0, 0, 0, QPixmap(1, 1))
        res.q_rect = dictionary["q_rect"]
        res.pixmap = dictionary["pixmapDto"].pixmap
        res.uuid = dictionary["uuid"]
        return res
