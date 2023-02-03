from PyQt6.QtWidgets import QMessageBox

from Action import Action
from FirstLoadDto import FirstLoadDto
from Message import Message
from SocketClient import SocketClient


class NetworkProxy:
    def __init__(self, socketClient: SocketClient):
        self.socketClient = socketClient
        self.connectingMessageBox = QMessageBox()
        self.connectingMessageBox.setText("Connecting...")
        self.sendQueue = self.socketClient.queue
        self.socketClient.start()
        self.connectingMessageBox.show()

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
        self.connectingMessageBox.close()
        self.socketClient.closeConnection()
        self.socketClient.disconnect()

    def connected(self):
        self.connectingMessageBox.close()

    def sendMessageToChat(self, msg):
        self.socketClient.sendChatMessage(msg)

    def firstLoad(self, objects):
        self.socketClient.sendFirstLoad(FirstLoadDto(objects))
