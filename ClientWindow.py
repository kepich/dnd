from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent, QCursor
from PyQt6.QtWidgets import QMainWindow, QWidgetAction, QToolBar, QMessageBox
from transliterate import translit

from EditModeEnum import EditMode
from EnterDialog import EnterDialog
from LocalProxy import LocalProxy
from NetworkProxy import NetworkProxy
from Playground import Playground
from SocketClient import SocketClient


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
        tool_bar.addAction(self.connectAction)
        tool_bar.addAction(self.disconnectAction)
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

        self.connectAction = QWidgetAction(self)
        self.connectAction.triggered.connect(self.connect)
        self.connectAction.setText("Connect")

        self.disconnectAction = QWidgetAction(self)
        self.disconnectAction.triggered.connect(self.disconnectSlot)
        self.disconnectAction.setEnabled(False)
        self.disconnectAction.setText("Disconnect")

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

    def connect(self):
        dlg = EnterDialog(self)
        if dlg.exec():
            print(f"Connecting to {dlg.addressTextBox.text()}:{dlg.portTextBox.text()}")
            canvas = self.playground.canvas
            canvas.networkProxy = NetworkProxy(
                SocketClient(dlg.addressTextBox.text(),
                             dlg.portTextBox.text(),
                             headers={
                                 "nickname": translit(dlg.nicknameTextBox.text(), language_code="ru", reversed=True)
                             }))
            self.connectSocketSignals(canvas)
            canvas.networkProxy.msgBox.show()

            self.connectAction.setEnabled(False)
            self.disconnectAction.setEnabled(True)

    def connectSocketSignals(self, canvas):
        canvas.networkProxy.socketClient.receivedSignal.connect(canvas.updateFromNetwork)
        canvas.networkProxy.socketClient.connectionEstablishedSignal.connect(self.connectionSlot)
        canvas.networkProxy.socketClient.connectionRejectedSignal.connect(self.disconnectSlot)
        canvas.networkProxy.socketClient.playerJoinSignal.connect(self.playerJoinSlot)
        canvas.networkProxy.socketClient.playerLeaveSignal.connect(self.playerLeaveSlot)

    def playerJoinSlot(self, nickname):
        print(translit(nickname, 'ru') + " join the game.")
        self.playground.rightPanel.addChatMessage("SERVER", translit(nickname, 'ru') + " join the game.")

    def playerLeaveSlot(self, nickname):
        print(translit(nickname, 'ru') + " leave the game.")
        self.playground.rightPanel.addChatMessage("SERVER", translit(nickname, 'ru') + " leave the game.")

    def disconnectSlot(self):
        canvas = self.playground.canvas
        canvas.networkProxy.msgBox.close()
        canvas.networkProxy.disconnect()
        canvas.networkProxy = LocalProxy()
        self.playground.rightPanel.clearChat()
        self.connectAction.setEnabled(True)
        self.disconnectAction.setEnabled(False)

        self.msgBox = QMessageBox()
        self.msgBox.setText("Disconnected")
        self.msgBox.show()

    def connectionSlot(self):
        canvas = self.playground.canvas
        canvas.networkProxy.msgBox.close()

    def keyPressEvent(self, ev: QKeyEvent) -> None:
        if ev.modifiers() & Qt.KeyboardModifier.ControlModifier:
            if ev.key() == Qt.Key.Key_V:
                point = self.mapFromParent(QCursor.pos())
                self.playground.canvas.paste(x_pos=point.x(), y_pos=point.y())
