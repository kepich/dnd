from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent, QCursor
from PyQt6.QtWidgets import QMainWindow, QWidgetAction, QToolBar

from EditModeEnum import EditMode
from Playground import Playground


class ClientWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("DnD")

        self.playground = Playground(self)
        self.setCentralWidget(self.playground)

        self.create_toolbar()
        self.showFullScreen()

    def create_toolbar(self):
        self.create_toolbar_actions()

        tool_bar = QToolBar("Tools")
        tool_bar.addAction(self.moveAction)
        tool_bar.addAction(self.resizeAction)
        tool_bar.addAction(self.deleteAction)
        tool_bar.addAction(self.drawAction)
        tool_bar.addAction(self.clearCanvasAction)
        tool_bar.addAction(self.undoAction)
        tool_bar.addAction(self.exitAction)

        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, tool_bar)

    def create_toolbar_actions(self):
        self.undoAction = QWidgetAction(self)
        self.undoAction.setText("Undo")
        self.undoAction.triggered.connect(self.playground.canvas.undo)

        self.moveAction = QWidgetAction(self)
        self.moveAction.setText("Move")
        self.moveAction.triggered.connect(self.set_mode_move)

        self.resizeAction = QWidgetAction(self)
        self.resizeAction.setText("Resize")
        self.resizeAction.triggered.connect(self.set_mode_resize)

        self.deleteAction = QWidgetAction(self)
        self.deleteAction.setText("Delete")
        self.deleteAction.triggered.connect(self.set_mode_delete)

        self.drawAction = QWidgetAction(self)
        self.drawAction.setText("Draw")
        self.drawAction.triggered.connect(self.set_mode_draw)
        self.drawAction.setEnabled(False)

        self.clearCanvasAction = QWidgetAction(self)
        self.clearCanvasAction.triggered.connect(self.playground.canvas.clearCanvasAction)
        self.clearCanvasAction.setText("Clear all")

        self.exitAction = QWidgetAction(self)
        self.exitAction.triggered.connect(self.close)
        self.exitAction.setText("Exit")

    def set_mode_move(self):
        self.playground.canvas.edit_mode = EditMode.MOVE
        self.enable_menu_buttons()
        self.moveAction.setEnabled(False)
        self.undoAction.setEnabled(False)

    def set_mode_resize(self):
        self.playground.canvas.edit_mode = EditMode.RESIZE
        self.enable_menu_buttons()
        self.resizeAction.setEnabled(False)
        self.undoAction.setEnabled(False)

    def set_mode_delete(self):
        self.playground.canvas.edit_mode = EditMode.DELETE
        self.enable_menu_buttons()
        self.deleteAction.setEnabled(False)
        self.undoAction.setEnabled(False)

    def set_mode_draw(self):
        self.playground.canvas.edit_mode = EditMode.DRAW
        self.enable_menu_buttons()
        self.drawAction.setEnabled(False)

    def enable_menu_buttons(self):
        self.moveAction.setEnabled(True)
        self.resizeAction.setEnabled(True)
        self.deleteAction.setEnabled(True)
        self.drawAction.setEnabled(True)
        self.clearCanvasAction.setEnabled(True)
        self.undoAction.setEnabled(True)

    def keyPressEvent(self, ev: QKeyEvent) -> None:
        if ev.modifiers() & Qt.KeyboardModifier.ControlModifier:
            if ev.key() == Qt.Key.Key_V:
                point = self.mapFromParent(QCursor.pos())
                self.playground.canvas.paste(x_pos=point.x(), y_pos=point.y())