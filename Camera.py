from PyQt6.QtCore import QRect


class Camera:
    x_offset = 0
    y_offset = 0

    MEASURE_MULTIPLIER = 1

    MAX_WIDTH = 1000
    MAX_HEIGHT = 1000

    def __init__(self, max_width, max_height):
        self.MAX_WIDTH = max_width
        self.MAX_HEIGHT = max_height

    def project(self, drawable_object):
        projected = QRect()

        projected.setX(self.rel(drawable_object.q_rect.x() + self.x_offset))
        projected.setRight(self.rel(drawable_object.q_rect.right() + self.x_offset))

        projected.setWidth(self.rel(drawable_object.q_rect.width()))
        projected.setHeight(self.rel(drawable_object.q_rect.height()))

        projected.setY(self.rel(drawable_object.q_rect.y() + self.y_offset))
        projected.setBottom(self.rel(drawable_object.q_rect.bottom() + self.y_offset))

        return projected

    def rel(self, v):
        return v * self.MEASURE_MULTIPLIER

    def abs(self, v):
        return v / self.MEASURE_MULTIPLIER

    def updateOffsets(self, dx, dy):
        self.x_offset = max(-self.MAX_WIDTH, min(0, self.x_offset + self.abs(dx)))
        self.y_offset = max(-self.MAX_HEIGHT, min(0, self.y_offset + self.abs(dy)))

    def updateMeasure(self, dm):
        self.MEASURE_MULTIPLIER = min(2.0, max(0.45, self.MEASURE_MULTIPLIER + dm))

    def x_rel(self, x):
        return -self.x_offset + self.abs(x)

    def y_rel(self, y):
        return -self.y_offset + self.abs(y)

    def abs_max_width(self):
        return self.abs(self.MAX_WIDTH)

    def abs_max_height(self):
        return self.abs(self.MAX_HEIGHT)

    def getCollide(self, x, y, objects):
        return next(filter(lambda obj: obj.is_collide(self.x_rel(x), self.y_rel(y)), objects), None)
