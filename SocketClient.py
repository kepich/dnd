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
    chatSignal = pyqtSignal(list)

    sio = socketio.Client()

    def __init__(self, ip, port, nickname):
        super().__init__()
        self.queue = []
        self.ip = ip
        self.port = port
        self.nickname = nickname
        self.headers = {"nickname": nickname}

        self.sio.on("connect", self.connectionEstablishedSignal.emit)
        self.sio.on("update", lambda msg: self.receivedSignal.emit(Message.fromBytes(msg)))
        self.sio.on("player_join", self.playerJoinSignal.emit)
        self.sio.on("player_leave", self.playerLeaveSignal.emit)
        self.sio.on("chat_msg", self.chatSignal.emit)

        self.isActive = True

    def run(self):
        try:
            self.sio.connect(f'http://{self.ip}:{self.port}', headers=self.headers)

            while self.isActive:
                if len(self.queue) > 0:
                    msg = self.queue[0]
                    self.queue.remove(msg)
                    self.sio.emit('broadcast_msg', msg.toBytes())
        except:
            traceback.print_exc()
            self.connectionRejectedSignal.emit()

    def closeConnection(self):
        self.sio.disconnect()
        self.isActive = False

    def sendChatMessage(self, msg: str):
        return self.sio.emit("chat_msg", msg)
