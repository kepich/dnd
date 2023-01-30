from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QColor, QPainter
from PyQt6.QtWidgets import QLabel


class Canvas(QLabel):

    def __init__(self, parent=None):
        super().__init__()

        if parent is not None:
            self.setParent(parent)

        self.last_x, self.last_y = None, None
        self.pen_color = QColor('#000000')

        self.clearAll()

    def set_pen_color(self, c):
        self.pen_color = QColor(c)

    def clearAll(self):
        pixmap = QPixmap(600, 300)
        pixmap.fill(Qt.GlobalColor.transparent)
        self.setPixmap(pixmap)

    def mouseMoveEvent(self, e):
        if self.last_x is None:  # First event.
            self.last_x = e.position().x()
            self.last_y = e.position().y()
            self.paintingActive()
            return  # Ignore the first time.

        pixmap = self.pixmap()
        painter = QPainter(pixmap)
        p = painter.pen()
        p.setWidth(4)
        p.setColor(self.pen_color)
        painter.begin(pixmap)
        painter.setPen(p)
        painter.drawLine(self.last_x, self.last_y, e.position().x(), e.position().y())
        painter.end()
        self.setPixmap(pixmap)

        # Update the origin for next time.
        self.last_x = e.position().x()
        self.last_y = e.position().y()

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None

    def clearCanvas(self):
        self.clearAll()
