from enum import Enum

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QColor, QPainter, QWheelEvent
from PyQt6.QtWidgets import QLabel, QApplication

from DrawableObject import DrawableObject

LINE_WIDTH = 4


class EditMode(Enum):
    DRAW = 1
    DELETE = 2
    MOVE = 3
    RESIZE = 4


class Canvas(QLabel):
    MAX_WIDTH = 1000
    MAX_HEIGHT = 1000

    MEASURE_MULTIPLIER = 1

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
            print(self.MEASURE_MULTIPLIER)
            self.last_draw = DrawableObject(
                e.position().x(),
                e.position().x(),
                e.position().y(),
                e.position().y(),
                QPixmap(self.original_cord(self.MAX_WIDTH), self.original_cord(self.MAX_HEIGHT)))

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

        p.setWidth(self.original_cord(LINE_WIDTH))
        painter.begin(self.last_draw.pixmap)
        painter.setPen(p)
        p.setWidth(LINE_WIDTH)
        painter.drawLine(self.original_cord(self.last_x),
                         self.original_cord(self.last_y),
                         self.original_cord(e.position().x()),
                         self.original_cord(e.position().y()))
        painter.end()

        self.last_draw.fit(self.original_cord(e.position().x()),
                           self.original_cord(e.position().y()),
                           self.original_cord(LINE_WIDTH))

        self.setPixmap(pixmap)

        self.last_x = e.position().x()
        self.last_y = e.position().y()

    def move_action(self, e):
        if self.last_x is None:
            self.last_x = e.position().x()
            self.last_y = e.position().y()

            self.last_draw = next(filter(
                lambda obj: obj.is_collide(self.original_cord(e.position().x()), self.original_cord(e.position().y())),
                self.objects), None)

            return

        if self.last_draw is not None:
            self.last_draw.move(self.original_cord(e.position().x() - self.last_x),
                                self.original_cord(e.position().y() - self.last_y))
            self.clear_all()
            self.redraw()

        self.last_x = e.position().x()
        self.last_y = e.position().y()

    def resize_action(self, e):
        if self.last_x is None:
            self.last_x = e.position().x()
            self.last_y = e.position().y()

            self.last_draw = next(filter(
                lambda obj: obj.is_collide(self.original_cord(e.position().x()), self.original_cord(e.position().y())),
                self.objects), None)

            return

        if self.last_draw is not None:
            self.last_draw.resize(self.original_cord(e.position().x() - self.last_x),
                                  self.original_cord(e.position().y() - self.last_y))
            self.clear_all()
            self.redraw()

        self.last_x = e.position().x()
        self.last_y = e.position().y()

    def mouseReleaseEvent(self, e):
        if self.edit_mode is EditMode.DRAW and self.last_draw is not None:
            self.last_draw.fit_pixmap()

            self.objects.append(self.last_draw)
            self.clear_all()
            self.redraw()
        elif self.edit_mode is EditMode.DELETE:
            delete_candidate = next(filter(
                lambda obj: obj.is_collide(self.original_cord(e.position().x()),
                                           self.original_cord(e.position().y())),
                self.objects), None)
            if delete_candidate is not None:
                self.objects.remove(delete_candidate)
                self.clear_all()
                self.redraw()

        self.last_x = None
        self.last_y = None
        self.last_draw = None

    def wheelEvent(self, event: QWheelEvent) -> None:
        numDegrees = event.angleDelta().y() / 16
        numSteps = numDegrees / 15

        self.MEASURE_MULTIPLIER = min(2.0, max(0.45, self.MEASURE_MULTIPLIER + numSteps))
        print(self.MEASURE_MULTIPLIER)
        self.clear_all()
        self.redraw()
        event.accept()

    def undo(self):
        self.clear_all()

        if len(self.objects) > 1:
            self.objects = self.objects[:-1]

            self.redraw()

    def paste(self, x_pos=0, y_pos=0):
        clipboard = QApplication.clipboard()
        mimeData = clipboard.mimeData()
        mimeData.imageData()
        if mimeData.hasImage():
            self.clear_all()
            new_object = DrawableObject(0, 0, 0, 0, QPixmap(1, 1))
            new_object.fromPixmapOnly(x_pos, y_pos, QPixmap(mimeData.imageData()))
            self.objects.append(new_object)
            self.redraw()

    def redraw(self):
        pixmap = self.pixmap()
        painter = QPainter(pixmap)
        painter.begin(pixmap)

        for pm in self.objects:
            print(str(pm.q_rect) + " -> " + str(pm.get_projected_rect(self.MEASURE_MULTIPLIER)))
            painter.drawPixmap(pm.get_projected_rect(self.MEASURE_MULTIPLIER), pm.pixmap)
        painter.end()
        self.setPixmap(pixmap)

    def clear_canvas(self):
        self.objects.clear()
        self.clear_all()

    def set_mode(self, mode):
        self.edit_mode = mode

    def original_cord(self, v):
        return v / self.MEASURE_MULTIPLIER
