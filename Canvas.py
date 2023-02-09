from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QColor, QPainter, QWheelEvent
from PyQt6.QtWidgets import QLabel, QApplication, QSizePolicy

from model.Message import Message
from model.Metadata import Metadata
from networking.Action import Action
from networking.Proxy import Proxy
from toolbar.EditMode import EditMode
from utils.Camera import Camera
from utils.UpdateLastDecorator import *

LINE_WIDTH = 4
GRID_LINE_WIDTH = 1
GRID_STEP = 50


class Canvas(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setParent(parent)

        self.isGridVisible = True
        self.sizePolicy().setHorizontalPolicy(QSizePolicy.Policy.Maximum)

        self.last_x, self.last_y = None, None
        self.dx_cumulative, self.dy_cumulative = None, None
        self.pen_color = QColor('#000000')
        self.objects: list[DrawableObject] = []
        self.last_draw = None

        self.isDarknessVisible = True
        self.isCave = False
        self.darknessValue = 0.90
        self.darknessFootage = QPixmap(100, 100)
        self.darknessFootage.fill(Qt.GlobalColor.black)

        self.camera = Camera(self.width(), self.height())
        self.networkProxy = Proxy()

        self.edit_mode = EditMode.DRAW
        self.redraw()

    def resizeCanvas(self, w, h):
        self.camera.MAX_WIDTH = w
        self.camera.MAX_HEIGHT = h
        self.redraw()

    def setPenColor(self, c):
        self.pen_color = QColor(c)

    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.MouseButton.LeftButton:
            if self.edit_mode is EditMode.DRAW:
                self.drawAction(e)
            elif self.edit_mode is EditMode.MOVE:
                self.moveAction(e)
            elif self.edit_mode is EditMode.RESIZE:
                self.resizeAction(e)
        elif e.buttons() == Qt.MouseButton.MiddleButton:
            self.fovMovingAction(e)

    @update_last(get_drawable)
    def drawAction(self, e):
        pixmap = self.pixmap()
        painter = QPainter(pixmap)
        p = painter.pen()
        p.setWidth(LINE_WIDTH)
        p.setColor(self.pen_color)
        painter.begin(pixmap)
        painter.setPen(p)
        painter.drawLine(self.last_x, self.last_y, e.position().x(), e.position().y())
        painter.end()

        p.setWidth(self.camera.abs(LINE_WIDTH))
        painter.begin(self.last_draw.pixmap)
        painter.setPen(p)
        painter.drawLine(self.camera.abs(self.last_x),
                         self.camera.abs(self.last_y),
                         self.camera.abs(e.position().x()),
                         self.camera.abs(e.position().y()))
        painter.end()

        self.last_draw.fit(self.camera.abs(e.position().x()),
                           self.camera.abs(e.position().y()),
                           self.camera.abs(LINE_WIDTH))

        self.setPixmap(pixmap)

    @update_last_cumulative(get_collide)
    def moveAction(self, e):
        if self.last_draw is not None:
            self.last_draw.move(self.camera.abs(e.position().x() - self.last_x),
                                self.camera.abs(e.position().y() - self.last_y))
            self.redraw()

    @update_last_cumulative(get_collide)
    def resizeAction(self, e):
        if self.last_draw is not None:
            self.last_draw.resize(self.camera.abs(e.position().x() - self.last_x),
                                  self.camera.abs(e.position().y() - self.last_y))
            self.redraw()

    @update_last(get_none)
    def fovMovingAction(self, e):
        self.camera.updateOffsets(e.position().x() - self.last_x, e.position().y() - self.last_y)
        self.redraw()

    def mouseReleaseEvent(self, e):
        if self.edit_mode is EditMode.DRAW and self.last_draw is not None:
            self.last_draw.fit_pixmap()
            self.last_draw.move(-self.camera.x_offset, -self.camera.y_offset)

            self.networkProxy.create(self.objects, self.last_draw)
            self.redraw()
        elif self.edit_mode is EditMode.DELETE:
            delete_candidate = self.camera.getCollide(e.position().x(), e.position().y(), self.objects)
            if delete_candidate is not None:
                self.networkProxy.remove(self.objects, delete_candidate)
                self.redraw()
        elif self.edit_mode is EditMode.MOVE and self.last_draw is not None:
            # TODO: Здесь можно сделать прилипание к сетке
            self.networkProxy.moveCumulative(self.last_draw,
                                             self.camera.abs(self.dx_cumulative),
                                             self.camera.abs(self.dy_cumulative))
        elif self.edit_mode is EditMode.RESIZE and self.last_draw is not None:
            self.networkProxy.resizeCumulative(self.last_draw,
                                               self.camera.abs(self.dx_cumulative),
                                               self.camera.abs(self.dy_cumulative))

        self.last_x = None
        self.last_y = None
        self.dx_cumulative = None
        self.dy_cumulative = None
        self.last_draw = None

    def wheelEvent(self, event: QWheelEvent) -> None:
        numDegrees = event.angleDelta().y() / 32
        numSteps = numDegrees / 15
        self.camera.updateMeasure(numSteps)
        self.redraw()

    def undo(self):
        if len(self.objects) > 0:
            self.networkProxy.remove(self.objects, self.objects[-1])

        self.redraw()

    def createEntityWithMetadata(self, pixmap: QPixmap, metadata: Metadata):
        if metadata.name is not None:
            duplicate = next(filter(lambda obj: obj.metadata.name == metadata.name, self.objects), None)

            if duplicate is not None:
                self.networkProxy.remove(self.objects, duplicate)

        newEntity = DrawableObject(0, 0, 0, 0)
        newEntity.from_pixmap_and_offset(pixmap, self.camera.x_abs(0), self.camera.y_abs(0))
        newEntity.metadata = metadata
        self.networkProxy.create(self.objects, newEntity)
        self.redraw()

    def paste(self, x_pos=0, y_pos=0):
        clipboard = QApplication.clipboard()
        mimeData = clipboard.mimeData()
        if mimeData.hasImage():
            pixmap = QPixmap(mimeData.imageData())

            self.last_draw = DrawableObject(self.camera.abs(x_pos),
                                            self.camera.abs(x_pos) + pixmap.width(),
                                            self.camera.abs(y_pos),
                                            self.camera.abs(y_pos) + pixmap.height())

            self.last_draw.from_pixmap_and_offset(pixmap,
                                                  self.camera.x_abs(x_pos - 85),
                                                  self.camera.y_abs(y_pos - 10))

            self.networkProxy.create(self.objects, self.last_draw)
            self.redraw()

    def clearCanvasAction(self):
        self.networkProxy.clear(self.objects)
        self.redraw()

    def drawGrid(self, pixmap):
        painter = QPainter(pixmap)
        p = painter.pen()
        p.setWidth(GRID_LINE_WIDTH)
        p.setColor(QColor('#999999'))
        painter.begin(pixmap)
        painter.setPen(p)

        rel_grid_step = self.camera.rel(GRID_STEP)
        temp_x = self.camera.x_offset_rel() % rel_grid_step
        temp_y = self.camera.y_offset_rel() % rel_grid_step

        while temp_x <= pixmap.width():
            painter.drawLine(temp_x, 0, temp_x, pixmap.height())
            temp_x = temp_x + rel_grid_step

        while temp_y <= pixmap.height():
            painter.drawLine(0, temp_y, pixmap.width(), temp_y)
            temp_y = temp_y + rel_grid_step

        painter.end()

    def redraw(self):
        self.clearAll()

        pixmap = self.pixmap()
        painter = QPainter(pixmap)
        painter.begin(pixmap)

        entities = []
        for pm in self.objects:
            if pm.isEntity():
                entities.append(pm)
            else:
                painter.drawPixmap(self.camera.project(pm), pm.pixmap)

        for pm in entities:
            rect = self.camera.project(pm)
            painter.drawPixmap(rect, pm.pixmap)
            painter.drawText(QPoint(rect.x(), rect.y() - 10), pm.getEntityHeader())

        painter.end()

        if self.isGridVisible:
            self.drawGrid(pixmap)

        painter.begin(pixmap)
        if self.isDarknessVisible:
            if self.isCave:
                painter.setOpacity(1)
            else:
                painter.setOpacity(self.darknessValue)
            painter.drawPixmap(pixmap.rect(), self.darknessFootage)
        painter.end()

        self.setPixmap(pixmap)

    def clearAll(self):
        pixmap = QPixmap(self.camera.MAX_WIDTH, self.camera.MAX_HEIGHT)
        pixmap.fill(Qt.GlobalColor.lightGray)
        self.setPixmap(pixmap)

    def resizeEvent(self, a0) -> None:
        self.camera.MAX_HEIGHT = self.parent().height() - 210
        self.camera.MAX_WIDTH = self.parent().width() - self.parent().rightPanel.width() - 50
        self.redraw()

    def setGridVisibility(self, status):
        self.isGridVisible = status
        self.redraw()

    def setDarknessVisibility(self, status):
        self.isDarknessVisible = status
        self.redraw()

    def setCaveDarkness(self, status):
        self.isCave = status
        self.redraw()

    def findObjectByUUID(self, uuid):
        return next(filter(lambda obj: str(obj.uuid) == uuid, self.objects), None)

    def updateFromNetwork(self, msg: Message):
        if msg.action is Action.CREATE:
            self.objects.append(DrawableObject.deserialize(msg.drawableObject))
        elif msg.action is Action.MOVE:
            obj: DrawableObject = self.findObjectByUUID(msg.uuid)
            obj.move(msg.dx, msg.dy)
        elif msg.action is Action.RESIZE:
            obj: DrawableObject = self.findObjectByUUID(msg.uuid)
            obj.resize(msg.dx, msg.dy)
        elif msg.action is Action.REMOVE:
            obj: DrawableObject = self.findObjectByUUID(msg.uuid)
            self.objects.remove(obj)
        elif msg.action is Action.CLEAR:
            self.objects.clear()

        self.redraw()

    def firstLoad(self):
        self.networkProxy.firstLoad(self.objects)

    def syncObjects(self, data: list[dict]):
        for obj in data:
            self.objects.append(DrawableObject.deserialize(obj))
        self.redraw()

    def storeGame(self) -> dict:
        return {
            "objects": [i.serialize() for i in self.objects],
            "darknessValue": self.darknessValue,
            "isDarknessVisible": True,
            "isCave": self.isCave
        }

    def restoreGame(self, state: dict):
        if "darknessValue" in state.keys():
            self.darknessValue = state["darknessValue"]

        if "isDarknessVisible" in state.keys():
            self.isDarknessVisible = state["isDarknessVisible"]

        self.isCave = state["isCave"]
        self.syncObjects(state["objects"])

    def storeScene(self):
        return {
            "objects": [i.serialize() for i in self.objects],
            "isCave": self.isCave
        }
