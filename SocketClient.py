import traceback

import socketio
from PyQt6.QtCore import QThread, pyqtSignal

from Message import Message


class SocketClient(QThread):
    receivedSignal = pyqtSignal(Message)
    connectionEstablishedSignal = pyqtSignal()
    connectionRejectedSignal = pyqtSignal()

    sio = socketio.Client()

    def __init__(self, ip, port):
        super().__init__()
        self.queue = []
        self.ip = ip
        self.port = port
        self.sio.on("connect", self.connect)
        self.sio.on("update", self.receive)
        self.isActive = True

    def run(self):
        try:
            self.sio.connect(f'http://{self.ip}:{self.port}')

            while self.isActive:
                # Try to send to server
                if len(self.queue) > 0:
                    msg = self.queue[0]
                    self.queue.remove(msg)
                    print(f"SEND: {msg}")
                    self.sio.emit('broadcast_msg', msg.toBytes())
        except:
            traceback.print_exc()
            self.connectionRejectedSignal.emit()

    def receive(self, msg):
        self.updateObjects(msg)

    def connect(self):
        print('Connection established!')
        self.connectionEstablishedSignal.emit()

    def updateObjects(self, msg):
        try:
            self.receivedSignal.emit(Message.fromBytes(msg))
        except:
            traceback.print_exc()

    def closeConnection(self):
        self.sio.disconnect()
        self.isActive = False

    def getMessageQueue(self):
        return self.queue
