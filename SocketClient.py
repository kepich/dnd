from PyQt6.QtCore import QThread, pyqtSignal
import traceback

from Message import Message


class SocketClient(QThread):
    receivedSignal = pyqtSignal(Message)

    def __init__(self, messageQueue):
        super().__init__()
        self.messageQueue = messageQueue

    def run(self):
        while True:
            # Try to send to server
            if len(self.messageQueue) > 0:
                msg = self.messageQueue[0]
                print("SEND: " + str(msg))
                self.messageQueue.remove(msg)
                self.sendToSocket(msg)

            # TODO: Try to read socket
            recieved = None
            if recieved is not None:
                self.updateObjects(recieved)

    def sendToSocket(self, msg):
        try:
            self.receivedSignal.emit(msg)
        except:
            traceback.print_exc()

    def updateObjects(self, msg):
        try:
            self.receivedSignal.emit(msg)
        except:
            traceback.print_exc()