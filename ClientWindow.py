from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QWidgetAction, QToolBar

from Playground import Playground

from enum import Enum

# class syntax
class EditMode(Enum):
    DRAW = 1
    SELECT = 2
    MOVE = 3
    RESIZE = 4

class ClientWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("DnD")
        self.setGeometry(100, 100, 600, 400)

        self.playground = Playground()
        self.setCentralWidget(self.playground)

        self._createToolBar()

        self.edit_mode = EditMode.DRAW


    def _createToolBar(self):
        self._createToolbarActions()

        tool_bar = QToolBar("Tools")
        tool_bar.addAction(self.moveAction)
        tool_bar.addAction(self.resizeAction)
        tool_bar.addAction(self.deleteAction)
        tool_bar.addAction(self.drawAction)
        tool_bar.addAction(self.clearCanvasAction)

        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, tool_bar)

    def _createToolbarActions(self):
        self.moveAction = QWidgetAction(self)
        self.moveAction.setText("Move")
        self.moveAction.triggered.connect(self.set_mode_MOVE)

        self.resizeAction = QWidgetAction(self)
        self.resizeAction.setText("Resize")
        self.resizeAction.triggered.connect(self.set_mode_RESIZE)

        self.deleteAction = QWidgetAction(self)
        self.deleteAction.setText("Delete")
        self.deleteAction.triggered.connect(self.set_mode_SELECT)

        self.drawAction = QWidgetAction(self)
        self.drawAction.setText("Draw")
        self.drawAction.triggered.connect(self.set_mode_DRAW)

        self.clearCanvasAction = QWidgetAction(self)
        self.clearCanvasAction.triggered.connect(self.playground.canvas.clearCanvas)
        self.clearCanvasAction.setText("Clear all")

    def set_mode_MOVE(self):
        print("EDIT MODE: MOVE")
        self.edit_mode = EditMode.MOVE
        self.playground.setDisabled(True)

    def set_mode_RESIZE(self):
        print("EDIT MODE: RESIZE")
        self.edit_mode = EditMode.RESIZE
        self.playground.setDisabled(True)

    def set_mode_SELECT(self):
        print("EDIT MODE: SELECT")
        self.edit_mode = EditMode.SELECT
        self.playground.setDisabled(True)

    def set_mode_DRAW(self):
        print("EDIT MODE: DRAW")
        self.edit_mode = EditMode.DRAW
        self.playground.setDisabled(False)
