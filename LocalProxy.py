class LocalProxy:
    def move(self, obj, x, y):
        obj.move(x, y)

    def resize(self, obj, x, y):
        obj.resize(x, y)

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
