class LocalProxy:
    def moveCumulative(self, obj, x, y):
        pass

    def resizeCumulative(self, obj, x, y):
        pass

    def create(self, collection, obj):
        collection.append(obj)

    def remove(self, collection, obj):
        collection.remove(obj)

    def clear(self, collection):
        collection.clear()

    def disconnect(self):
        pass

    def connected(self):
        pass

    def sendMessageToChat(self, msg):
        pass

    def firstLoad(self, objects):
        pass

    def weatherSend(self, objects):
        pass