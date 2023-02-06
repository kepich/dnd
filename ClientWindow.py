from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent, QCursor, QResizeEvent
from PyQt6.QtWidgets import QMainWindow, QWidgetAction, QToolBar, QMessageBox
from transliterate import translit

from EditMode import EditMode
from EnterDialog import EnterDialog
from LoadDialog import LoadDialog
from Playground import Playground
from SaveDialog import SaveDialog
from SaveManager import SaveManager
from SocketClient import SocketClient


class ClientWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("DnD")

        self.playground = Playground(self)
        self.setCentralWidget(self.playground)

        self.createToolBar()
        self.showMaximized()
        self.saveManager = SaveManager()

    def createToolBar(self):
        self.createToolBarActions()

        tool_bar = QToolBar("Tools")
        tool_bar.addAction(self.moveAction)
        tool_bar.addAction(self.resizeAction)
        tool_bar.addAction(self.deleteAction)
        tool_bar.addAction(self.drawAction)
        tool_bar.addAction(self.clearCanvasAction)
        tool_bar.addAction(self.undoAction)
        tool_bar.addAction(self.connectAction)
        tool_bar.addAction(self.disconnectAction)
        tool_bar.addAction(self.saveAction)
        tool_bar.addAction(self.loadAction)
        tool_bar.addAction(self.exitAction)

        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, tool_bar)

    def createToolBarActions(self):
        self.undoAction = QWidgetAction(self)
        self.undoAction.setText("Undo")
        self.undoAction.triggered.connect(self.playground.canvas.undo)

        self.moveAction = QWidgetAction(self)
        self.moveAction.setText("Move")
        self.moveAction.triggered.connect(self.setMoveMode)

        self.resizeAction = QWidgetAction(self)
        self.resizeAction.setText("Resize")
        self.resizeAction.triggered.connect(self.setResizeMode)

        self.deleteAction = QWidgetAction(self)
        self.deleteAction.setText("Delete")
        self.deleteAction.triggered.connect(self.setDeleteMode)

        self.drawAction = QWidgetAction(self)
        self.drawAction.setText("Draw")
        self.drawAction.triggered.connect(self.setDrawMode)
        self.drawAction.setEnabled(False)

        self.clearCanvasAction = QWidgetAction(self)
        self.clearCanvasAction.setText("Clear all")
        self.clearCanvasAction.triggered.connect(self.playground.canvas.clearCanvasAction)

        self.connectAction = QWidgetAction(self)
        self.connectAction.setText("Connect")
        self.connectAction.triggered.connect(self.connect)

        self.disconnectAction = QWidgetAction(self)
        self.disconnectAction.setEnabled(False)
        self.disconnectAction.setText("Disconnect")
        self.disconnectAction.triggered.connect(self.disconnectSlot)

        self.saveAction = QWidgetAction(self)
        self.saveAction.setText("Save")
        self.saveAction.triggered.connect(self.saveSlot)

        self.loadAction = QWidgetAction(self)
        self.loadAction.setText("Load")
        self.loadAction.triggered.connect(self.loadSlot)

        self.exitAction = QWidgetAction(self)
        self.exitAction.setText("Exit")
        self.exitAction.triggered.connect(self.close)

    def setMoveMode(self):
        self.playground.canvas.edit_mode = EditMode.MOVE
        self.enableMenuButtons()
        self.moveAction.setEnabled(False)
        self.undoAction.setEnabled(False)

    def setResizeMode(self):
        self.playground.canvas.edit_mode = EditMode.RESIZE
        self.enableMenuButtons()
        self.resizeAction.setEnabled(False)
        self.undoAction.setEnabled(False)

    def setDeleteMode(self):
        self.playground.canvas.edit_mode = EditMode.DELETE
        self.enableMenuButtons()
        self.deleteAction.setEnabled(False)
        self.undoAction.setEnabled(False)

    def setDrawMode(self):
        self.playground.canvas.edit_mode = EditMode.DRAW
        self.enableMenuButtons()
        self.drawAction.setEnabled(False)

    def enableMenuButtons(self):
        self.moveAction.setEnabled(True)
        self.resizeAction.setEnabled(True)
        self.deleteAction.setEnabled(True)
        self.drawAction.setEnabled(True)
        self.clearCanvasAction.setEnabled(True)
        self.undoAction.setEnabled(True)

    def connect(self):
        dlg = EnterDialog(self)
        if dlg.exec():
            socketClient = SocketClient(dlg.addressTextBox.text(),
                                        dlg.portTextBox.text(),
                                        translit(dlg.nicknameTextBox.text(), language_code="ru", reversed=True))
            self.playground.canvas.networkProxy.connect(socketClient)
            self.connectSocketSignals(socketClient)
            self.playground.rightPanel.chatWidget.nickname = dlg.nicknameTextBox.text()
            self.playground.rightPanel.chatWidget.clearChat()

            self.connectAction.setEnabled(False)
            self.disconnectAction.setEnabled(True)

    def connectSocketSignals(self, socketClient):
        socketClient.receivedSignal.connect(self.playground.canvas.updateFromNetwork)
        socketClient.connectionEstablishedSignal.connect(self.playground.canvas.networkProxy.connected)

        socketClient.connectionRejectedSignal.connect(self.disconnectSlot)

        socketClient.playerJoinSignal.connect(self.playerJoinSlot)
        socketClient.playerLeaveSignal.connect(self.playerLeaveSlot)
        socketClient.chatSignal.connect(self.addChatMessageSlot)

        socketClient.needFirstLoadSignal.connect(
            lambda: self.playground.canvas.networkProxy.firstLoad(self.playground.storeGame()))
        socketClient.loadSignal.connect(self.playground.restoreGame)

        socketClient.weatherTimeSignal.connect(self.playground.rightPanel.timeWidget.setCurrentTimeData)
        socketClient.masterFirstLoadSignal.connect(self.playground.rightPanel.setMaster)

        socketClient.caveDarknessSignal.connect(self.playground.rightPanel.setCaveDarkness)

    def addChatMessageSlot(self, message):
        self.playground.rightPanel.chatWidget.addChatMessage(message[0], message[1])

    def playerJoinSlot(self, nickname):
        self.playground.rightPanel.chatWidget.addChatMessage("SERVER", nickname + " join the game.")

    def playerLeaveSlot(self, nickname):
        self.playground.rightPanel.chatWidget.addChatMessage("SERVER", nickname + " leave the game.")

    def disconnectSlot(self):
        self.playground.canvas.networkProxy.disconnect()
        self.playground.rightPanel.chatWidget.clearChat()
        self.connectAction.setEnabled(True)
        self.disconnectAction.setEnabled(False)
        self.playground.rightPanel.timeWidget.endTime()

        disconnectMessageBox = QMessageBox()
        disconnectMessageBox.setText("Disconnected")
        disconnectMessageBox.show()

    def loadSlot(self):
        dlg = LoadDialog(self)
        if dlg.exec():
            loadedData = self.saveManager.load(dlg.getChosenSave())
            self.playground.restoreGame(loadedData)
            self.playground.canvas.networkProxy.sendLoad(loadedData)

    def saveSlot(self):
        dlg = SaveDialog(self)
        if dlg.exec():
            self.saveManager.save(dlg.saveNameTextBox.text(), self.playground.storeGame())

    def keyPressEvent(self, ev: QKeyEvent) -> None:
        if ev.modifiers() & Qt.KeyboardModifier.ControlModifier:
            if ev.key() == Qt.Key.Key_V:
                point = self.mapFromParent(QCursor.pos())
                self.playground.canvas.paste(x_pos=point.x(), y_pos=point.y())

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.playground.resizeEvent(a0)
