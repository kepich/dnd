from enum import Enum

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QColor, QPainter
from PyQt6.QtWidgets import QLabel

from DrawableObject import DrawableObject

LINE_WIDTH = 4


class EditMode(Enum):
    DRAW = 1
    DELETE = 2
    MOVE = 3
    RESIZE = 4


class Canvas(QLabel):
    MAX_WIDTH = 1200
    MAX_HEIGHT = 700

    def __init__(self, parent=None):
        super().__init__()

        if parent is not None:
            self.setParent(parent)

        self.last_x, self.last_y = None, None
        self.pen_color = QColor('#000000')
        self.objects = []
        self.last_draw = None

        self.edit_mode = EditMode.DRAW

        self.setStyleSheet("border: 1px solid black;")

        self.clear_all()

    def set_pen_color(self, c):
        self.pen_color = QColor(c)

    def clear_all(self):
        pixmap = QPixmap(self.MAX_WIDTH, self.MAX_HEIGHT)
        pixmap.fill(Qt.GlobalColor.transparent)
        self.setPixmap(pixmap)

    def mouseMoveEvent(self, e):
        if self.edit_mode is EditMode.DRAW:
            self.draw_action(e)
        elif self.edit_mode is EditMode.MOVE:
            self.move_action(e)
        elif self.edit_mode is EditMode.RESIZE:
            self.resize_action(e)

    def draw_action(self, e):
        if self.last_x is None:
            self.last_x = e.position().x()
            self.last_y = e.position().y()
            self.paintingActive()
            self.last_draw = DrawableObject(
                e.position().x(),
                e.position().x(),
                e.position().y(),
                e.position().y(),
                QPixmap(self.MAX_WIDTH, self.MAX_HEIGHT))

            return

        pixmap = self.pixmap()
        painter = QPainter(pixmap)
        p = painter.pen()
        p.setWidth(LINE_WIDTH)
        p.setColor(self.pen_color)
        painter.begin(pixmap)
        painter.setPen(p)
        painter.drawLine(self.last_x, self.last_y, e.position().x(), e.position().y())
        painter.end()

        painter.begin(self.last_draw.pixmap)
        painter.setPen(p)
        painter.drawLine(self.last_x, self.last_y, e.position().x(), e.position().y())
        painter.end()

        self.last_draw.fit(e.position().x(), e.position().y(), LINE_WIDTH)

        self.setPixmap(pixmap)

        self.last_x = e.position().x()
        self.last_y = e.position().y()

    def move_action(self, e):
        if self.last_x is None:
            self.last_x = e.position().x()
            self.last_y = e.position().y()

            self.last_draw = next(filter(
                lambda obj: obj.is_collide(e.position().x(), e.position().y()), self.objects), None)

            return

        if self.last_draw is not None:
            self.last_draw.move(e.position().x() - self.last_x, e.position().y() - self.last_y)
            self.clear_all()
            self.redraw()

        self.last_x = e.position().x()
        self.last_y = e.position().y()

    def resize_action(self, e):
        if self.last_x is None:
            self.last_x = e.position().x()
            self.last_y = e.position().y()

            self.last_draw = next(filter(
                lambda obj: obj.is_collide(e.position().x(), e.position().y()), self.objects), None)

            return

        if self.last_draw is not None:
            self.last_draw.resize(e.position().x() - self.last_x, e.position().y() - self.last_y)
            self.clear_all()
            self.redraw()

        self.last_x = e.position().x()
        self.last_y = e.position().y()

    def mouseReleaseEvent(self, e):
        if self.edit_mode is EditMode.DRAW:
            self.last_draw.fit_pixmap()

            self.objects.append(self.last_draw)
        elif self.edit_mode is EditMode.DELETE:
            delete_candidate = next(filter(
                lambda obj: obj.is_collide(e.position().x(), e.position().y()), self.objects), None)
            if delete_candidate is not None:
                self.objects.remove(delete_candidate)
                self.clear_all()
                self.redraw()

        self.last_x = None
        self.last_y = None
        self.last_draw = None

    def undo(self):
        self.clear_all()

        if len(self.objects) > 1:
            self.objects = self.objects[:-1]

            self.redraw()

    def redraw(self):
        pixmap = self.pixmap()
        painter = QPainter(pixmap)
        painter.begin(pixmap)
        for pm in self.objects:
            painter.drawPixmap(pm.q_rect, pm.pixmap)
        painter.end()
        self.setPixmap(pixmap)

    def clear_canvas(self):
        self.objects.clear()
        self.clear_all()

    def set_mode(self, mode):
        self.edit_mode = mode
