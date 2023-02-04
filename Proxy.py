from LocalProxy import LocalProxy
from NetworkProxy import NetworkProxy
from SocketClient import SocketClient


class Proxy:
    def __init__(self):
        self.localProxy = LocalProxy()
        self.tempProxy = self.localProxy

    def moveCumulative(self, obj, x, y):
        self.tempProxy.moveCumulative(obj, x, y)

    def resizeCumulative(self, obj, x, y):
        self.tempProxy.resizeCumulative(obj, x, y)

    def create(self, collection, obj):
        self.tempProxy.create(collection, obj)

    def remove(self, collection, obj):
        self.tempProxy.remove(collection, obj)

    def clear(self, collection):
        self.tempProxy.clear(collection)

    def sendMessageToChat(self, msg):
        self.tempProxy.sendMessageToChat(msg)

    def disconnect(self):
        self.tempProxy.disconnect()
        self.tempProxy = self.localProxy

    def connected(self):
        self.tempProxy.connected()

    def connect(self, socketClient: SocketClient):
        self.tempProxy = NetworkProxy(socketClient)

    def firstLoad(self, objects):
        self.tempProxy.firstLoad(objects)