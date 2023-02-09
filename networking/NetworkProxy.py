from PyQt6.QtWidgets import QMessageBox

from model.Message import Message
from model.Metadata import Metadata
from networking.Action import Action
from networking.SocketClient import SocketClient


class NetworkProxy:
    def __init__(self, socketClient: SocketClient):
        self.socketClient = socketClient
        self.connectingMessageBox = QMessageBox()
        self.connectingMessageBox.setText("Connecting...")
        self.sendQueue = self.socketClient.queue
        self.socketClient.start()
        self.connectingMessageBox.show()

    def moveCumulative(self, obj, x, y):
        self.sendQueue.append(Message(Action.MOVE, uuid=str(obj.uuid), dx=x, dy=y))

    def resizeCumulative(self, obj, x, y):
        self.sendQueue.append(Message(Action.RESIZE, uuid=str(obj.uuid), dx=x, dy=y))

    def create(self, collection, obj):
        collection.append(obj)
        self.sendQueue.append(Message(Action.CREATE, drawableObject=obj))

    def remove(self, collection, obj):
        collection.remove(obj)
        self.sendQueue.append(Message(Action.REMOVE, uuid=str(obj.uuid)))

    def updateMeta(self, meta: Metadata):
        self.sendQueue.append(Message(Action.UPDATE_META, meta=meta))

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
        self.socketClient.sendFirstLoad(objects)

    def weatherSend(self, objects):
        self.socketClient.sendWeather(objects)

    def caveSend(self, value):
        self.socketClient.caveSend(value)

    def sendLoad(self, data):
        self.socketClient.sendLoad(data)

