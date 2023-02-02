from PyQt6.QtWidgets import QMessageBox

from Message import Message, Action
from SocketClient import SocketClient


class NetworkProxy:
    def __init__(self, socketClient: SocketClient):
        self.socketClient = socketClient
        self.msgBox = QMessageBox()
        self.msgBox.setText("Connecting...")
        self.sendQueue = self.socketClient.getMessageQueue()
        self.socketClient.start()

    def move(self, obj, x, y):
        obj.move(x, y)
        self.sendQueue.append(Message(Action.MOVE, uuid=str(obj.uuid), dx=x, dy=y))

    def resize(self, obj, x, y):
        obj.resize(x, y)
        self.sendQueue.append(Message(Action.RESIZE, uuid=str(obj.uuid), dx=x, dy=y))

    def create(self, collection, obj):
        collection.append(obj)
        self.sendQueue.append(Message(Action.CREATE, drawableObject=obj))

    def remove(self, collection, obj):
        collection.remove(obj)
        self.sendQueue.append(Message(Action.REMOVE, uuid=str(obj.uuid)))

    def clear(self, collection):
        collection.clear()
        self.sendQueue.append(Message(Action.CLEAR))

    def disconnect(self):
        self.socketClient.closeConnection()
        self.socketClient.disconnect()
