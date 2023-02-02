import traceback

import socketio
from PyQt6.QtCore import QThread, pyqtSignal

from Message import Message


class SocketClient(QThread):
    receivedSignal = pyqtSignal(Message)
    connectionEstablishedSignal = pyqtSignal()
    connectionRejectedSignal = pyqtSignal()
    playerJoinSignal = pyqtSignal(str)
    playerLeaveSignal = pyqtSignal(str)

    sio = socketio.Client()

    def __init__(self, ip, port, headers):
        super().__init__()
        self.queue = []
        self.ip = ip
        self.port = port
        self.headers = headers
        self.sio.on("connect", self.connectionEstablishedSignal.emit)
        self.sio.on("update", self.receive)
        self.sio.on("player_join", self.playerJoinSignal.emit)
        self.sio.on("player_leave", self.playerLeaveSignal.emit)
        self.isActive = True

    def run(self):
        try:
            self.sio.connect(f'http://{self.ip}:{self.port}', headers=self.headers)

            while self.isActive:
                # Try to send to server
                if len(self.queue) > 0:
                    msg = self.queue[0]
                    self.queue.remove(msg)
                    self.sio.emit('broadcast_msg', msg.toBytes())
        except:
            traceback.print_exc()
            self.connectionRejectedSignal.emit()

    def receive(self, msg):
        try:
            self.receivedSignal.emit(Message.fromBytes(msg))
        except:
            traceback.print_exc()

    def closeConnection(self):
        self.sio.disconnect()
        self.isActive = False

    def getMessageQueue(self):
        return self.queue
